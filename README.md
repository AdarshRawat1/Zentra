<p align="center">
  <img width="150" alt="glitch" src="https://github.com/user-attachments/assets/68c96547-cc6f-41ed-9001-21d4905976c6" />
</p>

# Zentra: AI-Powered Task Automation Chrome Extension


Zentra is a powerful Chrome extension designed to streamline your workflow by automating repetitive tasks using the power of AI. With support for multiple underlying AI models, Zentra offers flexible and intelligent automation tailored to your needs.

## ✨ Features

* **Intelligent Task Automation:** Automate common web tasks with AI-driven precision.
* **Multi-Model Support:** Choose from various AI models to best suit your automation requirements and preferences.
* **Seamless Integration:** Works directly within your Chrome browser for a smooth user experience.
* **Customizable Workflows:** Define and customize automation routines to fit your unique processes.
* **Privacy-Focused:** Designed with user privacy in mind, ensuring your data remains secure.

## 🚀 Demo

See Zentra in action!

[![Zentra Demo Recording Placeholder](https://placehold.co/600x300/cccccc/333333?text=Zentra+Demo+Video)](https://drive.google.com/drive/folders/1_50mA_AYyS8H6tHjUfYVnHRx5pK4Szz1?usp=drive_link)
*(Click the image to watch a demo video of Zentra)*

## 🛠️ Setup and Installation

Follow these steps to install and set up Zentra in your Chrome browser:

1.  **Download the Extension:**
    * **Option 1 (Chrome Web Store - Coming Soon):** Once available, you can install Zentra directly from the [Chrome Web Store](https://chrome.google.com/webstore/category/extensions).
    * **Option 2 (Manual Installation - For Developers/Testing):**
        * Download the latest release of Zentra from the [releases page](https://github.com/your-repo/zentra/releases) on GitHub (or clone this repository).
        * Unzip the downloaded file if it's a `.zip` archive.

2.  **Load in Chrome:**
    * Open Chrome and navigate to `chrome://extensions`.
    * Enable **"Developer mode"** by toggling the switch in the top right corner.
    * Click on **"Load unpacked"** button.
    * Browse to the unzipped Zentra extension folder (the one containing `manifest.json`) and select it.

3.  **Pin Zentra to your Toolbar (Recommended):**
    * After installation, you'll see the Zentra icon in your extensions list (puzzle piece icon) next to your profile picture.
    * Click the puzzle piece icon, find "Zentra", and then click the pin icon next to it to pin it to your Chrome toolbar for easy access.

4.  **Configure AI Models (Optional):**
    * Click on the Zentra icon in your toolbar.
    * Access the settings or configuration panel (usually a gear icon or "Options").
    * Here, you can select your preferred AI model(s) and configure any necessary API keys or credentials.

## 🤝 Contributing

---

We welcome contributions! If you'd like to contribute to Zentra, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes and commit them (`git commit -m 'Add new feature'`).
4.  Push to the branch (`git push origin feature/your-feature-name`).
5.  Open a Pull Request.

Please ensure your code adheres to the existing style and includes relevant tests.

## 📄 License


Zentra is released under the [MIT License](LICENSE).

## 📞 Support

---

If you encounter any issues or have questions, please open an issue on our [GitHub repository](https://github.com/your-repo/zentra/issues).

## Developer guide

### What Zentra is built with

Zentra is a TypeScript browser extension for AI-assisted browser automation. Its background service worker runs a Planner, Navigator, and Validator flow: it interprets a task, interacts with browser pages, then checks whether the task is complete. The project includes a browser-use-derived JSON schema with local changes; it is not identified as a direct fork.

The codebase is a pnpm workspace managed by Turborepo. It uses Node.js, TypeScript, Vite, React, Tailwind CSS, Chrome Extension Manifest V3 APIs, LangChain provider integrations, Zod, and `fflate` for extension archives. A schema utility explicitly says its schema was exported from browser-use v0.1.41 with modifications.

### Main capabilities

- Natural-language browser tasks from the side panel, including progress display, stop controls, task history, and saved prompts.
- Page navigation and interaction, including search, URL navigation, clicks, text entry, scrolling, and tab management.
- Separate model configuration for the Planner, Navigator, and Validator.
- Providers including OpenAI, Anthropic, DeepSeek, Gemini, Grok, Ollama, Azure OpenAI, OpenRouter, Groq, Cerebras, and custom OpenAI-compatible endpoints.
- General behavior settings, site allow/deny lists, and optional speech-to-text.
- Chrome and Firefox development/build flows; Firefox builds omit Chrome's side panel API.

Provider credentials and extension settings are saved in browser extension storage, not `.env`. Browser automation requires broad page access and debugger/scripting permissions declared in the extension manifest. Configure a provider and models in the extension's Options page before submitting tasks.

### Project layout

- `chrome-extension/src/background`: extension service worker, browser context, task execution, agents, prompts, and browser actions.
- `chrome-extension/manifest.js`: generated Manifest V3 configuration and browser-specific settings.
- `chrome-extension/public`: static assets, permission UI, and injected DOM helper.
- `pages/side-panel`: task/chat UI, history, favorites, and task progress.
- `pages/options`: model, general, and site-blocking settings.
- `pages/content`: content script entry point.
- `packages/storage`: typed settings and chat-history persistence.
- `packages/shared`, `packages/ui`: reusable UI helpers and components.
- `packages/hmr`, `packages/vite-config`, `packages/dev-utils`: build and development tooling.
- `packages/i18n`: locale messages and build helpers.
- `packages/zipper`: ZIP/XPI archive creation.
- `dist`: generated unpacked extension bundle; `dist-zip`: generated timestamped release archives.

### Prerequisites and first run

- Node.js 22.12.0 or newer (`.nvmrc` specifies 22.12.0).
- pnpm 9.15.1 (`packageManager` is pinned in `package.json`).
- Chrome for the standard flow, plus credentials/model configuration for at least the agents you plan to use. Ollama can run locally.

From the repository root in PowerShell:

```powershell
corepack enable
corepack prepare pnpm@9.15.1 --activate
pnpm install --frozen-lockfile
pnpm dev
```

Open `chrome://extensions`, enable **Developer mode**, choose **Load unpacked**, and select the repository's `dist` directory. Reload the extension after changes; refresh the website tab when its content script changed. Use the extension card's **Inspect views** links to debug its service worker and pages.

For a production-style bundle, run `pnpm build`. For Firefox, use `pnpm dev:firefox` or `pnpm build:firefox`. Create a Chrome ZIP with `pnpm zip` or a Firefox XPI with `pnpm zip:firefox`; archives go into `dist-zip`.

### Clean builds and old output

```powershell
# Remove built extension output and rebuild
pnpm clean:bundle
pnpm build

# Clear only Turbo's task cache
pnpm clean:turbo

# Remove dependencies and reinstall from the lockfile
pnpm clean:install

# Full cleanup, reinstall, and build
pnpm clean
pnpm install --frozen-lockfile
pnpm build
```

`pnpm clean:bundle` clears `dist` and package bundle outputs. It does not remove old archives from `dist-zip`; to remove those archives too, run:

```powershell
Remove-Item -Recurse -Force .\dist-zip -ErrorAction SilentlyContinue
```

Rebuilding does not clear settings or chat history saved in the browser. Remove/reset extension storage in the browser separately if you intend to clear that data.

### Task execution flow

1. The side panel sends a task to the background service worker through a runtime port.
2. The background task manager reads model and general settings, then creates an executor.
3. The Planner decides whether browser work is needed and can outline steps.
4. The Navigator observes page context and invokes registered browser actions; progress events are sent back to the panel.
5. The Validator checks completion. The executor can continue, fail, or return a result.
6. Chat history and settings are stored through the extension storage package.

Useful checks are `pnpm type-check` and `pnpm lint`. The root lint command includes automatic fixes, so it can modify files. Package-level test scripts exist, but there is no root aggregate test command.

### Notes

- Use ordinary HTTP/HTTPS tabs; browser-internal pages generally cannot be automated by extensions.
- For model errors, check provider credentials, selected model per agent, endpoint settings, and local model connectivity.
- The repository currently has conflicting license metadata: `package.json` says Apache-2.0, while `LICENSE` and this README say MIT. Resolve this before redistributing.
