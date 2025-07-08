# 🔧 JSONify

A Streamlit-based multi-tool for working with JSON — build, convert, format, and validate with ease.

## 🚀 Features

- 🔤 **String Converter**  
  Convert any text (code, prompts, special characters, etc.) into a valid JSON string, escaped and ready for APIs.

- 🗂️ **JSON Object Builder**  
  Visually create key-value pairs with type selectors (string, number, boolean, null, array, object). Great for generating or editing structured data.

- 🔄 **JSON Formatter**  
  Beautify messy JSON, validate structure, and explore schema and stats — line counts, depth, types, and more.

- 🔍 **Live Validator**  
  Drop in any JSON snippet and instantly check its validity, size, and structure.

- 📦 **Import & Export**  
  Copy, paste, or upload files. Get minified or pretty outputs. All formats supported.

- 🧠 **LLM-Optimized**  
  Designed for editing prompt templates, serialized inputs, and structured examples used in generative AI workflows.

## 🖼️ UI Preview

> 🎥 Add a GIF or screenshot here for bonus style  
> _(Use [carbon.now.sh](https://carbon.now.sh/) or [Licecap](https://www.cockos.com/licecap/) for quick screen recordings)_

## 🔧 Installation

```bash
git clone https://github.com/yourusername/jsonify.git
cd jsonify
pip install -r requirements.txt
streamlit run streamlit_app.py
````

## 🛠 Built With

* [Streamlit](https://streamlit.io/)
* [Python 3.10+](https://www.python.org/)
* `json`, `re`, and `typing` modules
* 💡 Custom UI/UX with embedded CSS

## 📚 Use Case Examples

* Editing OpenAI or Anthropic prompt templates
* Cleaning up long strings from scripts, responses, or logs
* Building config objects for API calls or test frameworks
* Converting messy form data into structured payloads

## 📥 File Support

* `.txt`, `.json`, `.csv`, `.py`, `.html`, `.md`, `.xml`, `.yml`, `.js`, `.css`
* URL fetching for JSON data
* UTF-8 and fallback encoding support

## 💡 Pro Tips

* Use **"Copy for Code"** for safely escaped strings
* The builder automatically handles nested objects and arrays
* Drag-and-drop JSON import for fast editing

## 👨‍💻 Author

Made with ⚙️ by [Abhimanyu Jaiswal](https://github.com/CodexAbhi)
For anyone tired of manually quoting strings and debugging malformed brackets.

## 🧪 Status

> ⚠️ Just a personal tool that turned out to be surprisingly useful.
> May or may not be maintained, depending on my coffee supply ☕️

## 📄 License

MIT License

```
