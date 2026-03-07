---
title: "Reverse Engineering a Tauri App — Because the API Wasn't Good Enough"
date: 2024-03-20
description: "How I used Frida to peek inside a Tauri desktop app, intercept WebSocket traffic, and figure out what it was actually doing."
tags: ["Reverse Engineering", "Tauri", "Frida", "Security"]
categories: ["Tech"]
showToc: true
---

## The Itch

There was a desktop app I needed to understand. Not crack, not steal from — just *understand*. The official docs were vague, the API was undocumented, and the app did something interesting under the hood that I wanted to replicate.

It was built with Tauri. Great framework, genuinely impressed by it. But from a reverse engineering perspective? It's a bit of a pain. Here's why, and here's how I got through it anyway.

---

## Why Tauri Is Annoying to Reverse Engineer

Most Electron apps are embarrassingly easy to poke at — the JS is right there, sometimes literally unminified. Tauri is different:

**1. Rust binaries are not your friend.**
Rust compiles to highly optimized native code with minimal debug symbols. There's no convenient bytecode to inspect. You're looking at assembly, and lots of it.

**2. Encryption everywhere.**
Tauri apps often use `ring` (Rust's crypto library) for AES, ChaCha20, and friends. The good stuff is buried behind encryption layers that make traffic interception useless on its own.

**3. WebSocket + IPC = hidden conversations.**
The Rust backend and the web frontend talk to each other constantly via WebSocket or Tauri's IPC bridge. None of that is visible by default.

So. Dynamic analysis it is.

---

## The Toolkit

- **Frida** — the star of the show. Dynamic instrumentation, hooks into running processes, speaks JavaScript. Indispensable.
- **Wireshark / mitmproxy** — for anything HTTP-based that leaks before encryption kicks in.
- **Ghidra** — for when you want to stare at assembly until it starts making sense (or you give up).
- **A lot of patience.**

---

## The Approach

The goal: intercept WebSocket messages and cryptographic operations at the *function call* level, before encryption and after decryption. Frida lets you do exactly this by hooking exported symbols from the binary.

Here's the script I used to monitor a module called `grass` (the target app). Adapt the module name for your target:

```javascript
function monitorGrass() {
    console.log("[*] Starting monitor...");
    
    const grassModule = Process.enumerateModules()
        .find(m => m.name.toLowerCase().includes('grass'));
    
    if (!grassModule) {
        console.log('[!] Module not found');
        return;
    }
    
    // What we care about
    const patterns = [
        /websocket/i,
        /ring.*encrypt/i,
        /ring.*decrypt/i,
        /aes/i,
        /grass/i,
        /hyper/i,
        /ws.*connect/i,
        /ws.*message/i,
    ];

    // Noise we don't care about
    const ignorePatterns = [
        /__rust_dealloc/,
        /__rust_alloc/,
        /drop/i,
        /clone/i,
        /debug/i,
        /TokioSleep/,
        /poll/,
    ];

    grassModule.enumerateExports().forEach(exp => {
        if (ignorePatterns.some(p => p.test(exp.name))) return;
        if (!patterns.some(p => p.test(exp.name))) return;
        if (exp.type !== 'function') return;

        try {
            Interceptor.attach(exp.address, {
                onEnter(args) {
                    console.log(`\n[CALL] ${exp.name}`);
                    for (let i = 0; i < 4; i++) {
                        try {
                            const s = args[i].readUtf8String();
                            if (s && s.length > 0 && s.length < 1000)
                                console.log(`\tArg${i}: ${s}`);
                        } catch(e) {
                            console.log(`\tArg${i}: 0x${args[i]}`);
                        }
                    }
                },
                onLeave(retval) {
                    try {
                        const s = retval.readUtf8String();
                        if (s && s.length > 0 && s.length < 1000)
                            console.log(`\tReturn: ${s}`);
                    } catch(e) {}
                }
            });
            console.log(`[+] Hooked: ${exp.name}`);
        } catch(e) {
            console.log(`[-] Failed: ${exp.name} — ${e}`);
        }
    });

    console.log("[*] Done. Watching...");
}

setImmediate(monitorGrass);
```

Run it with:
```bash
frida -l monitor.js -n YourAppName
```

---

## What You'll See

Once the hooks are in place and you start using the app, your terminal starts lighting up. You'll see function names, argument values (when they're readable strings), and return values. 

The key insight: by hooking *before* encryption and *after* decryption, you see plaintext even when the wire traffic is encrypted. This is what makes Frida so powerful for this kind of work.

---

## The Part Where I Feel Compelled to Add a Disclaimer

This is a technique, not a weapon. Use it on software you have the right to analyze — your own apps, security research, CTF challenges, understanding something you paid for. Don't use it to steal, spy, or cheat.

Also, some apps have anti-tamper mechanisms. If your target crashes the moment Frida attaches, that's intentional. You'll need to dig deeper, which is a whole other post.

---

## What I Actually Found

The app was doing something clever with its WebSocket keep-alive — rotating auth tokens on a schedule that wasn't documented anywhere. Once I could see the plaintext messages, the pattern was obvious. Took about 20 minutes to replicate in my own code.

Worth the detour.
