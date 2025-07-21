import dns.resolver
import json

# 你的主域名
DOMAIN = "elan.us.kg"
# 可维护的常用子域名列表（可根据实际情况扩展）
SUBDOMAINS = [
    "libretv", "blog", "app", "status", "monitor", "service1", "service2", "finlive", "pecker", "hawk"
]

results = []
for sub in SUBDOMAINS:
    fqdn = f"{sub}.{DOMAIN}"
    try:
        answers = dns.resolver.resolve(fqdn, 'CNAME')
        for rdata in answers:
            results.append({
                "name": sub,
                "fqdn": fqdn,
                "cname": str(rdata.target).rstrip('.')
            })
    except Exception:
        continue

with open("data/services.json", "w") as f:
    json.dump(results, f, indent=2) 