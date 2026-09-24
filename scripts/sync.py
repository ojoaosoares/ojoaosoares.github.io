#!/usr/bin/env python3
"""
Automated Data Synchronizer for João Soares Portfolio.
Fetches public data from:
  - GitHub REST API (public repos, stars, activity)
  - ORCID Public REST API (publications, book chapters, conference papers, DOIs)
  - Local Profile Configuration (LinkedIn details, experiences, education)
Generates data/portfolio_data.json
"""

import json
import os
import urllib.request
import urllib.error
import datetime

CONFIG = {
    "github_username": "ojoaosoares",
    "orcid_id": "0009-0002-7600-9784",
    "lattes_url": "https://lattes.cnpq.br/1035800800676947",
    "linkedin_url": "https://www.linkedin.com/in/ojoaovsoares",
    "email": "joaosoares@dcc.ufmg.br",
    "name": "João Soares",
    "institution": "Universidade Federal de Minas Gerais (UFMG)",
    "location": "Belo Horizonte, MG, Brasil"
}

def fetch_json(url, headers=None):
    if headers is None:
        headers = {}
    headers.setdefault("User-Agent", "Mozilla/5.0 (Portfolio-Sync-Bot)")
    headers.setdefault("Accept", "application/vnd.github+json")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"Warning: Failed to fetch {url}: {e}")
        return None

def sync_github(username):
    print(f"Fetching GitHub profile for {username}...")
    user_data = fetch_json(f"https://api.github.com/users/{username}")
    repos_data = fetch_json(f"https://api.github.com/users/{username}/repos?per_page=100&sort=pushed") or []

    # Curated fallbacks for repos with missing topics or descriptions on GitHub
    default_topics = {
        "GPSR-NS3": ["ns-3", "c++", "routing", "simulation"],
        "Location-Service-NS3": ["ns-3", "c++", "manet", "routing"],
        "unbound_AF_XDP": ["af_xdp", "ebpf", "dns", "c"],
        "xv6-riscv-lottery-scheduler": ["c", "risc-v", "kernel", "os"],
        "xhttp": ["ebpf", "xdp", "c", "kernel-bypass", "http"],
        "indexer-and-query-processor": ["spimi", "v-byte", "bm25", "search-engine"],
        "KIDDS": ["systems", "kernel", "ebpf"],
        "RIP": ["networking", "routing", "python"],
        "mock-packet-parser": ["python", "networking", "packets"],
        "web-crawler": ["python", "crawler", "automation"],
        "exploring-code-evolution": ["git", "software-engineering", "code-analysis"],
        "encryption-lab": ["cryptography", "security", "python"],
        "Minimum-Path": ["algorithms", "graphs", "c++"],
        "Carmichael-Numbers": ["number-theory", "algorithms", "c++"],
        "Teacher-Pay-Student-Performance": ["data-analysis", "python", "jupyter"],
        "atividade-semana-3-iJunior": ["typescript", "web"]
    }

    default_descriptions = {
        "Location-Service-NS3": "Location Service implementation in ns-3 simulator for mobile ad-hoc networks (MANET).",
        "unbound_AF_XDP": "High-performance recursive DNS resolver accelerated with AF_XDP and eBPF in-kernel processing.",
        "RIP": "Routing Information Protocol (RIP) implementation in Python.",
        "mock-packet-parser": "Network packet parser and packet analysis utility in Python.",
        "PyJupyter": "Interactive Jupyter environment and Python utilities.",
        "web-crawler": "Automated web crawler and scraper built with Python.",
        "encryption-lab": "Cryptographic algorithms and security protocols laboratory.",
        "Minimum-Path": "Shortest path algorithms and graph analysis in C++.",
        "Carmichael-Numbers": "Carmichael numbers analysis and primality testing algorithms in C++.",
        "Teacher-Pay-Student-Performance": "Data science analysis on education metrics and student performance.",
        "atividade-semana-3-iJunior": "Web development activities and exercises in TypeScript."
    }

    # Filter out forks or keep interesting repos
    curated_repos = []
    featured_names = [
        "AtesN-DS",
        "curriculum-gen",
        "indexer-and-query-processor",
        "GPSR-NS3",
        "xv6-riscv-lottery-scheduler",
        "xdp_ping",
        "DPDK_ping",
        "xhttp",
        "QuantumSimulator",
        "KIDDS",
        "unbound_AF_XDP"
    ]

    total_stars = 0
    for r in repos_data:
        name = r.get("name")
        if not name:
            continue
        # Exclude special user profile readme repo or any obsidian notes vault
        if name.lower() == username.lower() or "obsidian" in name.lower():
            continue

        stars = r.get("stargazers_count", 0)
        total_stars += stars

        if name in featured_names or not r.get("fork"):
            topics = r.get("topics") or []
            if not topics:
                topics = default_topics.get(name, [r.get("language")] if r.get("language") else [])

            desc = r.get("description") or default_descriptions.get(name, "")

            curated_repos.append({
                "name": name,
                "full_name": r.get("full_name"),
                "description": desc,
                "html_url": r.get("html_url"),
                "language": r.get("language") or "Code",
                "topics": topics,
                "stars": stars,
                "forks": r.get("forks_count", 0),
                "updated_at": r.get("pushed_at"),
                "is_featured": name in featured_names
            })

    return {
        "username": username,
        "public_repos": user_data.get("public_repos", len(repos_data)) if user_data else len(repos_data),
        "total_stars": total_stars,
        "repos": curated_repos
    }

def sync_orcid(orcid_id):
    if not orcid_id:
        return []
    print(f"Fetching ORCID works for {orcid_id}...")
    url = f"https://pub.orcid.org/v3.0/{orcid_id}/works"
    headers = {"Accept": "application/json"}
    data = fetch_json(url, headers)
    if not data or "group" not in data:
        return []

    publications = []
    for group in data.get("group", []):
        summaries = group.get("work-summary", [])
        if not summaries:
            continue
        work = summaries[0]

        title_obj = work.get("title", {}) or {}
        title_val = (title_obj.get("title") or {}).get("value", "Untitled")
        
        journal_val = ""
        if work.get("journal-title"):
            journal_val = work.get("journal-title", {}).get("value", "")

        pub_type = work.get("type", "publication")
        
        pub_year = ""
        pub_date = work.get("publication-date")
        if pub_date and pub_date.get("year"):
            pub_year = pub_date.get("year", {}).get("value", "")

        doi_url = ""
        external_ids = work.get("external-ids", {}).get("external-id", [])
        for ext in external_ids:
            if ext.get("external-id-type") == "doi":
                ext_url = (ext.get("external-id-url") or {}).get("value")
                if ext_url:
                    doi_url = ext_url
                else:
                    val = ext.get("external-id-value")
                    if val:
                        doi_url = f"https://doi.org/{val}"
                break

        url_val = (work.get("url") or {}).get("value") or doi_url

        publications.append({
            "title": title_val,
            "venue": journal_val,
            "year": pub_year,
            "type": pub_type,
            "url": url_val,
            "doi": doi_url
        })

    return publications

def main():
    print("Starting automated synchronization...")
    github_info = sync_github(CONFIG["github_username"])
    orcid_pubs = sync_orcid(CONFIG["orcid_id"])

    payload = {
        "last_sync": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "profile": {
            "name": CONFIG["name"],
            "institution": CONFIG["institution"],
            "location": CONFIG["location"],
            "email": CONFIG["email"],
            "github_username": CONFIG["github_username"],
            "github_url": f"https://github.com/{CONFIG['github_username']}",
            "orcid_id": CONFIG["orcid_id"],
            "orcid_url": f"https://orcid.org/{CONFIG['orcid_id']}",
            "lattes_url": CONFIG["lattes_url"],
            "linkedin_url": CONFIG["linkedin_url"]
        },
        "github": github_info,
        "orcid": orcid_pubs
    }

    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "portfolio_data.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"Successfully synced data to {output_path}!")
    print(f"  GitHub Repos: {len(github_info['repos'])}")
    print(f"  ORCID Works: {len(orcid_pubs)}")

if __name__ == "__main__":
    main()
