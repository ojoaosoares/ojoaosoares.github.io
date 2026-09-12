# João Soares · Portfólio de Engenharia & Pesquisa

Portfólio acadêmico e profissional de **João Soares**, pesquisador no **LECOM/UFMG** (eBPF/XDP) e engenheiro de software na **Tarken**. Desenvolvido como uma página estática moderna, de alta performance e minimalista em tons de preto profundo (`#08080b`) e amarelo/dourado (`#f5c542`).

---

## ✦ Principais Recursos

- **Design Minimalista & Elegante:** Paleta preto profundo com detalhes em amarelo/dourado e tipografia refinada (`Cinzel`, `Inter`, `JetBrains Mono`).
- **Sincronização Automática (GitHub & ORCID):** GitHub Action agendada (`.github/workflows/sync.yml`) que consulta as APIs públicas do GitHub e do ORCID para manter repositórios, estrelas e artigos científicos atualizados sem intervenção manual.
- **Bilinguismo Nativo (PT-BR / EN):** Alternância instantânea de idioma via interface e atalhos, com estado preservado no navegador (`localStorage`).
- **Currículo Integrado:** Download direto do currículo em PDF (`curriculo.pdf` em português e `resume.pdf` em inglês).
- **Background Atmosférico Interativo:** Canvas HTML5 nativo e suave com partículas estelares e constelações discretas (60fps, ultra-leve, respeitando `prefers-reduced-motion`).
- **Filtro de Projetos Dinâmico:** Navegação por categorias (Sistemas & Kernel, Web & Automação, Algoritmos & Redes).
- **Totalmente Gratuito:** Compatível com GitHub Pages sem custos de hospedagem.

---

## 🚀 Como Publicar Gratuitamente no GitHub Pages

1. **Crie ou renomeie o repositório no seu GitHub:**
   - Crie um repositório chamado `ojoaosoares.github.io` (usando seu nome de usuário).
2. **Suba o código:**
   ```bash
   git remote set-url origin https://github.com/ojoaosoares/ojoaosoares.github.io.git
   git add .
   git commit -m "feat: portfolio minimalista preto e amarelo com auto-sync"
   git push -u origin main
   ```
3. **Ative o GitHub Pages:**
   - No GitHub, vá em **Settings** > **Pages**.
   - Em **Build and deployment** > **Source**, selecione `Deploy from a branch`.
   - Escolha a branch `main` e a pasta `/ (root)`.
   - Clique em **Save**.
4. Em poucos instantes, seu site estará no ar gratuitamente em:
   👉 **`https://ojoaosoares.github.io/`**

---

## 🔄 Como Funciona a Atualização Automática

O projeto inclui um pipeline automatizado em `.github/workflows/sync.yml` e o script `scripts/sync.py`:

- **GitHub API:** Puxa automaticamente estatísticas, repositórios públicos, estrelas e linguagens.
- **ORCID API:** Consulta as publicações cadastradas no ORCID (`0009-0002-7600-9784`), importando títulos, anos, periódicos e links DOI oficiais.
- **Execução Automática:** A Action roda automaticamente todo domingo à meia-noite (ou você pode disparar manualmente na aba **Actions** > **Run workflow**).
- Se houver novos artigos no ORCID ou repositórios no GitHub, o bot faz commit e push do arquivo `data/portfolio_data.json`, atualizando o site na hora.

---

## 💻 Teste e Execução Local

Abra `index.html` diretamente no navegador ou inicie um servidor HTTP local:

```bash
# Servidor local simples com Python
python3 -m http.server 8000
```

Acesse em: `http://localhost:8000`

Para testar a sincronização manualmente:
```bash
python3 scripts/sync.py
```

---

## 📁 Estrutura do Projeto

```text
.
├── index.html                  # Interface completa, estilização, animações e lógica
├── favicon.svg                 # Ícone minimalista em preto e dourado
├── profile.png                 # Foto de perfil
├── curriculo.pdf               # Currículo em Português
├── resume.pdf                  # Currículo em Inglês
├── robots.txt                  # Regras para indexadores de busca
├── sitemap.xml                 # Mapa do site para SEO
├── scripts/
│   └── sync.py                 # Script de sincronização automática com GitHub e ORCID
├── data/
│   └── portfolio_data.json     # Dados sincronizados automaticamente
├── .github/
│   └── workflows/
│       └── sync.yml            # Automação agendada via GitHub Actions
└── README.md                   # Documentação do projeto
```

---

## 📜 Licença

Distribuído sob a licença [MIT](LICENSE).
