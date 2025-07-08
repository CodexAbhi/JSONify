import streamlit as st
import json
import re
from typing import Any, Dict, List, Tuple

st.set_page_config(
    page_title="JSON String Converter & Object Builder",
    page_icon="🔧",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .copy-feedback {
        background-color: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
        border: 1px solid #c3e6cb;
    }
    .stButton > button {
        width: 100%;
    }
    .json-output {
        font-family: 'Courier New', monospace;
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
    }
    .pair-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #007bff;
    }
    .error-container {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
        border: 1px solid #f5c6cb;
    }
    .success-container {
        background-color: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
        border: 1px solid #c3e6cb;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'kv_pairs' not in st.session_state:
        st.session_state.kv_pairs = [{"key": "", "value": "", "type": "string", "id": 0}]
    if 'pair_counter' not in st.session_state:
        st.session_state.pair_counter = 1
    if 'last_json_output' not in st.session_state:
        st.session_state.last_json_output = ""

def add_new_pair():
    """Add a new key-value pair"""
    new_pair = {
        "key": "",
        "value": "",
        "type": "string",
        "id": st.session_state.pair_counter
    }
    st.session_state.kv_pairs.append(new_pair)
    st.session_state.pair_counter += 1

def remove_pair(pair_id: int):
    """Remove a pair by ID"""
    st.session_state.kv_pairs = [
        pair for pair in st.session_state.kv_pairs 
        if pair["id"] != pair_id
    ]
    # Ensure at least one pair exists
    if not st.session_state.kv_pairs:
        st.session_state.kv_pairs = [{"key": "", "value": "", "type": "string", "id": st.session_state.pair_counter}]
        st.session_state.pair_counter += 1

def clear_all_pairs():
    """Clear all pairs and reset to single empty pair"""
    st.session_state.kv_pairs = [{"key": "", "value": "", "type": "string", "id": st.session_state.pair_counter}]
    st.session_state.pair_counter += 1

def validate_json_string(json_str: str) -> Tuple[bool, str]:
    """Validate JSON string and return status with message"""
    try:
        json.loads(json_str)
        return True, "Valid JSON"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}"

def safe_json_parse(value_str: str, default_value: Any = None):
    """Safely parse JSON string with fallback"""
    if not value_str.strip():
        return default_value
    try:
        return json.loads(value_str)
    except json.JSONDecodeError:
        return value_str

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"

def copy_to_clipboard_js(text: str, success_message: str = "Copied to clipboard!"):
    """Generate JavaScript to copy text to clipboard"""
    # Escape special characters for JavaScript
    escaped_text = text.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
    
    st.markdown(f"""
    <script>
    (function() {{
        const text = `{escaped_text}`;
        if (navigator.clipboard && window.isSecureContext) {{
            navigator.clipboard.writeText(text).then(function() {{
                console.log('Copied to clipboard successfully');
            }}).catch(function(err) {{
                console.error('Failed to copy: ', err);
            }});
        }} else {{
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.opacity = '0';
            document.body.appendChild(textArea);
            textArea.select();
            try {{
                document.execCommand('copy');
                console.log('Copied using fallback method');
            }} catch (err) {{
                console.error('Fallback copy failed: ', err);
            }}
            document.body.removeChild(textArea);
        }}
    }})();
    </script>
    """, unsafe_allow_html=True)

# Initialize session state
initialize_session_state()

# Header
st.title("🔧 JSON String Converter & Object Builder")
st.markdown("Convert any input to JSON strings or build JSON objects from key-value pairs")

# Sidebar with tools
with st.sidebar:
    st.header("🛠️ Tools")
    
    # JSON Validator
    st.subheader("🔍 JSON Validator")
    json_to_validate = st.text_area(
        "Paste JSON to validate:",
        placeholder='{"key": "value"}',
        height=100,
        key="validator_input"
    )
    
    if json_to_validate:
        is_valid, message = validate_json_string(json_to_validate)
        if is_valid:
            st.success(f"✅ {message}")
            try:
                parsed = json.loads(json_to_validate)
                st.info(f"📊 Type: {type(parsed).__name__}")
                if isinstance(parsed, dict):
                    st.info(f"🔑 Keys: {len(parsed)}")
                elif isinstance(parsed, list):
                    st.info(f"📝 Items: {len(parsed)}")
            except:
                pass
        else:
            st.error(f"❌ {message}")
    
    st.divider()
    
    # Quick Actions
    st.subheader("⚡ Quick Actions")
    if st.button("🔄 Reset All", help="Clear all data and start fresh"):
        for key in list(st.session_state.keys()):
            if key.startswith(('kv_pairs', 'pair_counter', 'last_json_output')):
                del st.session_state[key]
        initialize_session_state()
        st.rerun()

# Mode selection
mode = st.radio(
    "Choose mode:",
    ["🔤 String Converter", "🗂️ JSON Object Builder", "🔄 JSON Formatter"],
    horizontal=True
)

if mode == "🔤 String Converter":
    # String Converter Mode
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Input")
        
        # Input method selection
        input_method = st.selectbox(
            "Choose input method:",
            ["Text Input", "Multi-line Text", "File Upload", "URL Input"]
        )
        
        input_text = ""
        
        if input_method == "Text Input":
            input_text = st.text_input(
                "Enter your text:",
                placeholder="Type anything here...",
                help="Single line text input"
            )
            
        elif input_method == "Multi-line Text":
            input_text = st.text_area(
                "Enter your text:", 
                placeholder="Type or paste multiple lines here...\nSupports newlines and special characters",
                height=200,
                help="Multi-line text input with support for special characters"
            )
            
        elif input_method == "URL Input":
            url_input = st.text_input(
                "Enter URL to fetch content:",
                placeholder="https://example.com/api/data",
                help="Fetch content from a URL (must be accessible)"
            )
            
            if url_input and st.button("🌐 Fetch URL Content"):
                try:
                    import urllib.request
                    import urllib.error
                    
                    with urllib.request.urlopen(url_input) as response:
                        content = response.read()
                        try:
                            input_text = content.decode('utf-8')
                            st.success(f"✅ Successfully fetched {format_file_size(len(content))} from URL")
                        except UnicodeDecodeError:
                            input_text = content.decode('latin-1')
                            st.warning("⚠️ Used Latin-1 encoding as fallback")
                            
                except urllib.error.URLError as e:
                    st.error(f"❌ Error fetching URL: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")
            
        elif input_method == "File Upload":
            uploaded_file = st.file_uploader(
                "Upload a text file",
                type=['txt', 'json', 'csv', 'py', 'js', 'html', 'css', 'md', 'xml', 'yaml', 'yml'],
                help="Supported formats: TXT, JSON, CSV, Python, JavaScript, HTML, CSS, Markdown, XML, YAML"
            )
            
            if uploaded_file is not None:
                try:
                    content = uploaded_file.read()
                    file_size = len(content)
                    
                    # Try UTF-8 first, then fallback to other encodings
                    encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii']
                    decoded_content = None
                    used_encoding = None
                    
                    for encoding in encodings:
                        try:
                            decoded_content = content.decode(encoding)
                            used_encoding = encoding
                            break
                        except UnicodeDecodeError:
                            continue
                    
                    if decoded_content is not None:
                        input_text = decoded_content
                        st.success(f"✅ File '{uploaded_file.name}' loaded successfully!")
                        st.info(f"📊 Size: {format_file_size(file_size)} | Encoding: {used_encoding.upper()}")
                    else:
                        st.error("❌ Could not decode file with any supported encoding")
                        
                except Exception as e:
                    st.error(f"❌ Error reading file: {str(e)}")

    with col2:
        st.subheader("✨ JSON String Output")
        
        if input_text:
            try:
                # Basic JSON string conversion
                json_string = json.dumps(input_text, ensure_ascii=False)
                
                # Display result
                st.code(json_string, language="json")
                
                # Action buttons
                col_copy1, col_copy2 = st.columns(2)
                
                with col_copy1:
                    if st.button("📋 Copy JSON String", key="copy_string", use_container_width=True):
                        copy_to_clipboard_js(json_string)
                        st.success("✅ Copied to clipboard!")
                
                with col_copy2:
                    # Escaped version for code
                    escaped_for_code = json_string.replace('\\', '\\\\').replace('"', '\\"')
                    if st.button("📋 Copy for Code", key="copy_escaped", use_container_width=True):
                        copy_to_clipboard_js(f'"{escaped_for_code}"')
                        st.success("✅ Code-ready version copied!")
                
                # Stats
                original_lines = input_text.count('\n') + 1 if input_text else 0
                st.info(f"📊 Original: {len(input_text)} chars, {original_lines} lines | JSON: {len(json_string)} chars")
                
                # Advanced options
                with st.expander("🔧 Advanced Options"):
                    col_adv1, col_adv2 = st.columns(2)
                    
                    with col_adv1:
                        ascii_only = st.checkbox("ASCII Only", help="Escape non-ASCII characters")
                        sort_keys = st.checkbox("Sort Keys", help="Sort object keys (if applicable)")
                    
                    with col_adv2:
                        indent_level = st.selectbox("Indentation", [None, 2, 4], help="Pretty print with indentation")
                    
                    if ascii_only or sort_keys or indent_level:
                        try:
                            advanced_json = json.dumps(
                                input_text,
                                ensure_ascii=ascii_only,
                                sort_keys=sort_keys,
                                indent=indent_level
                            )
                            st.code(advanced_json, language="json")
                            
                            if st.button("📋 Copy Advanced JSON", key="copy_advanced"):
                                copy_to_clipboard_js(advanced_json)
                                st.success("✅ Advanced JSON copied!")
                        except Exception as e:
                            st.error(f"❌ Error with advanced options: {str(e)}")
                
                # Validation preview
                with st.expander("🔍 Validation Preview"):
                    try:
                        parsed_back = json.loads(json_string)
                        st.text_area("Parsed back:", value=str(parsed_back), height=100, disabled=True)
                        
                        if parsed_back == input_text:
                            st.success("✅ Perfect match - JSON string is valid!")
                        else:
                            st.warning("⚠️ Mismatch detected - this shouldn't happen for strings")
                            
                    except Exception as e:
                        st.error(f"❌ Parse error: {str(e)}")
                        
            except Exception as e:
                st.error(f"❌ Error converting to JSON: {str(e)}")
        else:
            st.info("👈 Enter text on the left to see JSON string output")

elif mode == "🗂️ JSON Object Builder":
    # JSON Object Builder Mode
    st.subheader("🗂️ Build JSON Object from Key-Value Pairs")
    
    col1, col2 = st.columns([1.2, 0.8])
    
    with col1:
        st.markdown("#### Manage Key-Value Pairs")
        
        # Control buttons
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("➕ Add Pair", use_container_width=True):
                add_new_pair()
                st.rerun()
        
        with col_btn2:
            if st.button("🗑️ Clear All", use_container_width=True):
                clear_all_pairs()
                st.rerun()
        
        with col_btn3:
            if st.button("📋 Import JSON", use_container_width=True):
                st.session_state.show_import = True
        
        # Import JSON dialog
        if st.session_state.get('show_import', False):
            with st.container():
                st.markdown("**Import JSON Object:**")
                import_json = st.text_area(
                    "Paste JSON object to import:",
                    placeholder='{"key1": "value1", "key2": 123}',
                    height=100
                )
                
                col_import1, col_import2 = st.columns(2)
                with col_import1:
                    if st.button("✅ Import", key="confirm_import"):
                        try:
                            imported_data = json.loads(import_json)
                            if isinstance(imported_data, dict):
                                # Clear existing pairs and import new ones
                                st.session_state.kv_pairs = []
                                for key, value in imported_data.items():
                                    value_type = "string"
                                    if isinstance(value, bool):
                                        value_type = "boolean"
                                    elif isinstance(value, (int, float)):
                                        value_type = "number"
                                    elif isinstance(value, list):
                                        value_type = "array"
                                        value = json.dumps(value)
                                    elif isinstance(value, dict):
                                        value_type = "object"
                                        value = json.dumps(value)
                                    elif value is None:
                                        value_type = "null"
                                        value = ""
                                    
                                    st.session_state.kv_pairs.append({
                                        "key": key,
                                        "value": value,
                                        "type": value_type,
                                        "id": st.session_state.pair_counter
                                    })
                                    st.session_state.pair_counter += 1
                                
                                st.session_state.show_import = False
                                st.success(f"✅ Imported {len(imported_data)} pairs!")
                                st.rerun()
                            else:
                                st.error("❌ Please provide a JSON object (not array or primitive)")
                        except json.JSONDecodeError as e:
                            st.error(f"❌ Invalid JSON: {str(e)}")
                
                with col_import2:
                    if st.button("❌ Cancel", key="cancel_import"):
                        st.session_state.show_import = False
                        st.rerun()
                
                st.divider()
        
        # Display all pairs
        valid_pairs = []
        
        for i, pair in enumerate(st.session_state.kv_pairs):
            with st.container():
                # Use custom styling for pair container
                st.markdown('<div class="pair-container">', unsafe_allow_html=True)
                
                # Header with pair number and remove button
                col_header, col_remove = st.columns([3, 1])
                with col_header:
                    st.markdown(f"**Pair {i+1}:**")
                with col_remove:
                    if st.button(f"🗑️", key=f"remove_{pair['id']}", help=f"Remove pair {i+1}"):
                        remove_pair(pair['id'])
                        st.rerun()
                
                # Key and type inputs
                col_key, col_type = st.columns([2, 1])
                with col_key:
                    key = st.text_input(
                        "Key:",
                        value=pair["key"],
                        key=f"key_{pair['id']}",
                        placeholder="Enter key name"
                    )
                with col_type:
                    value_type = st.selectbox(
                        "Type:",
                        ["string", "number", "boolean", "null", "array", "object"],
                        index=["string", "number", "boolean", "null", "array", "object"].index(pair["type"]),
                        key=f"type_{pair['id']}"
                    )
                
                # Value input based on type
                value = None
                error_msg = None
                
                if value_type == "string":
                    value = st.text_input(
                        "Value:",
                        value=str(pair["value"]) if pair["value"] is not None else "",
                        key=f"value_{pair['id']}",
                        placeholder="Enter string value"
                    )
                
                elif value_type == "number":
                    try:
                        default_val = float(pair["value"]) if pair["value"] and pair["value"] != "" else 0.0
                    except (ValueError, TypeError):
                        default_val = 0.0
                    value = st.number_input(
                        "Value:",
                        value=default_val,
                        key=f"value_{pair['id']}",
                        help="Enter a number (integer or decimal)"
                    )
                
                elif value_type == "boolean":
                    current_bool = pair["value"]
                    if isinstance(current_bool, str):
                        current_bool = current_bool.lower() == "true"
                    elif not isinstance(current_bool, bool):
                        current_bool = False
                    
                    value = st.selectbox(
                        "Value:",
                        [True, False],
                        index=0 if current_bool else 1,
                        key=f"value_{pair['id']}"
                    )
                
                elif value_type == "null":
                    value = None
                    st.text("Value: null")
                
                elif value_type == "array":
                    value_str = st.text_area(
                        "Array (JSON format):",
                        value=str(pair["value"]) if pair["value"] else "[]",
                        key=f"value_{pair['id']}",
                        height=80,
                        placeholder='["item1", "item2", 123]',
                        help="Enter a valid JSON array"
                    )
                    
                    try:
                        if value_str.strip():
                            parsed_value = json.loads(value_str)
                            if isinstance(parsed_value, list):
                                value = parsed_value
                            else:
                                error_msg = "Value must be a JSON array"
                                value = value_str
                        else:
                            value = []
                    except json.JSONDecodeError as e:
                        error_msg = f"Invalid JSON array: {str(e)}"
                        value = value_str
                
                elif value_type == "object":
                    value_str = st.text_area(
                        "Object (JSON format):",
                        value=str(pair["value"]) if pair["value"] else "{}",
                        key=f"value_{pair['id']}",
                        height=80,
                        placeholder='{"nested": "value"}',
                        help="Enter a valid JSON object"
                    )
                    
                    try:
                        if value_str.strip():
                            parsed_value = json.loads(value_str)
                            if isinstance(parsed_value, dict):
                                value = parsed_value
                            else:
                                error_msg = "Value must be a JSON object"
                                value = value_str
                        else:
                            value = {}
                    except json.JSONDecodeError as e:
                        error_msg = f"Invalid JSON object: {str(e)}"
                        value = value_str
                
                # Show error if any
                if error_msg:
                    st.error(error_msg)
                
                # Update session state
                st.session_state.kv_pairs[i]["key"] = key
                st.session_state.kv_pairs[i]["value"] = value
                st.session_state.kv_pairs[i]["type"] = value_type
                
                # Add to valid pairs if key is not empty and no errors
                if key.strip() and not error_msg:
                    valid_pairs.append((key.strip(), value))
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.divider()
    
    with col2:
        st.markdown("#### JSON Object Output")
        
        if valid_pairs:
            try:
                # Build JSON object
                json_obj = {}
                for key, value in valid_pairs:
                    json_obj[key] = value
                
                # Convert to formatted JSON string
                json_output = json.dumps(json_obj, indent=2, ensure_ascii=False)
                st.session_state.last_json_output = json_output
                
                # Display JSON
                st.code(json_output, language="json")
                
                # Action buttons
                if st.button("📋 Copy JSON Object", key="copy_object", use_container_width=True):
                    copy_to_clipboard_js(json_output)
                    st.success("✅ Copied to clipboard!")
                
                # Minified version
                with st.expander("📦 Minified Version"):
                    minified = json.dumps(json_obj, separators=(',', ':'), ensure_ascii=False)
                    st.code(minified, language="json")
                    
                    if st.button("📋 Copy Minified", key="copy_minified", use_container_width=True):
                        copy_to_clipboard_js(minified)
                        st.success("✅ Minified version copied!")
                
                # Schema info
                with st.expander("📊 Object Schema"):
                    def get_schema_info(obj, path=""):
                        info = []
                        if isinstance(obj, dict):
                            for k, v in obj.items():
                                current_path = f"{path}.{k}" if path else k
                                type_name = type(v).__name__
                                if isinstance(v, dict):
                                    info.append(f"🔹 {current_path}: object ({len(v)} properties)")
                                    info.extend(get_schema_info(v, current_path))
                                elif isinstance(v, list):
                                    info.append(f"🔹 {current_path}: array ({len(v)} items)")
                                    if v and isinstance(v[0], (dict, list)):
                                        info.extend(get_schema_info(v[0], f"{current_path}[0]"))
                                else:
                                    info.append(f"🔹 {current_path}: {type_name}")
                        return info
                    
                    schema_info = get_schema_info(json_obj)
                    for info in schema_info:
                        st.text(info)
                
                # Stats
                st.info(f"📊 Properties: {len(json_obj)} | Characters: {len(json_output)}")
                
            except Exception as e:
                st.error(f"❌ Error building JSON: {str(e)}")
        else:
            st.info("👈 Add key-value pairs on the left to build JSON object")
            if st.session_state.kv_pairs and not any(pair["key"].strip() for pair in st.session_state.kv_pairs):
                st.warning("⚠️ Please enter key names for your pairs")

elif mode == "🔄 JSON Formatter":
    # JSON Formatter Mode
    st.subheader("🔄 JSON Formatter & Beautifier")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Input JSON")
        
        # Input methods for JSON
        json_input_method = st.selectbox(
            "Choose input method:",
            ["Paste JSON", "Upload JSON File", "Use Last Object Builder Output"]
        )
        
        input_json = ""
        
        if json_input_method == "Paste JSON":
            input_json = st.text_area(
                "Paste your JSON here:",
                placeholder='{"key": "value", "array": [1, 2, 3]}',
                height=300
            )
        
        elif json_input_method == "Upload JSON File":
            json_file = st.file_uploader(
                "Upload JSON file",
                type=['json'],
                help="Upload a .json file to format"
            )
            
            if json_file is not None:
                try:
                    content = json_file.read()
                    input_json = content.decode('utf-8')
                    st.success(f"✅ File '{json_file.name}' loaded successfully!")
                except Exception as e:
                    st.error(f"❌ Error reading file: {str(e)}")
        
        elif json_input_method == "Use Last Object Builder Output":
            if st.session_state.last_json_output:
                input_json = st.session_state.last_json_output
                st.info("✅ Using output from JSON Object Builder")
            else:
                st.warning("⚠️ No output available from Object Builder. Please build an object first.")
    
    with col2:
        st.markdown("#### Formatted Output")
        
        if input_json:
            try:
                # Parse JSON
                parsed_json = json.loads(input_json)
                
                # Formatting options
                st.markdown("**Formatting Options:**")
                col_opt1, col_opt2 = st.columns(2)
                
                with col_opt1:
                    indent_size = st.selectbox("Indentation:", [2, 4, 8], index=0)
                    sort_keys_fmt = st.checkbox("Sort Keys", value=False)
                
                with col_opt2:
                    ensure_ascii_fmt = st.checkbox("ASCII Only", value=False)
                    compact_fmt = st.checkbox("Compact Arrays", value=False)
                
                # Format JSON
                if compact_fmt:
                    # Custom compact formatting for arrays
                    formatted_json = json.dumps(
                        parsed_json,
                        indent=indent_size,
                        sort_keys=sort_keys_fmt,
                        ensure_ascii=ensure_ascii_fmt,
                        separators=(',', ': ')
                    )
                else:
                    formatted_json = json.dumps(
                        parsed_json,
                        indent=indent_size,
                        sort_keys=sort_keys_fmt,
                        ensure_ascii=ensure_ascii_fmt
                    )
                
                # Display formatted JSON
                st.code(formatted_json, language="json")
                
                # Action buttons
                col_action1, col_action2 = st.columns(2)
                
                with col_action1:
                    if st.button("📋 Copy Formatted", key="copy_formatted", use_container_width=True):
                        copy_to_clipboard_js(formatted_json)
                        st.success("✅ Formatted JSON copied!")
                
                with col_action2:
                    # Minified version
                    minified_json = json.dumps(parsed_json, separators=(',', ':'), ensure_ascii=ensure_ascii_fmt)
                    if st.button("📦 Copy Minified", key="copy_minified_fmt", use_container_width=True):
                        copy_to_clipboard_js(minified_json)
                        st.success("✅ Minified JSON copied!")
                
                # Analysis section
                with st.expander("📊 JSON Analysis"):
                    def analyze_json(obj, depth=0):
                        analysis = {
                            'total_keys': 0,
                            'max_depth': depth,
                            'types': {},
                            'arrays': 0,
                            'objects': 0
                        }
                        
                        if isinstance(obj, dict):
                            analysis['objects'] += 1
                            analysis['total_keys'] += len(obj)
                            for key, value in obj.items():
                                value_type = type(value).__name__
                                analysis['types'][value_type] = analysis['types'].get(value_type, 0) + 1
                                
                                if isinstance(value, (dict, list)):
                                    sub_analysis = analyze_json(value, depth + 1)
                                    analysis['total_keys'] += sub_analysis['total_keys']
                                    analysis['max_depth'] = max(analysis['max_depth'], sub_analysis['max_depth'])
                                    analysis['arrays'] += sub_analysis['arrays']
                                    analysis['objects'] += sub_analysis['objects']
                                    
                                    for t, count in sub_analysis['types'].items():
                                        analysis['types'][t] = analysis['types'].get(t, 0) + count
                        
                        elif isinstance(obj, list):
                            analysis['arrays'] += 1
                            for item in obj:
                                if isinstance(item, (dict, list)):
                                    sub_analysis = analyze_json(item, depth + 1)
                                    analysis['total_keys'] += sub_analysis['total_keys']
                                    analysis['max_depth'] = max(analysis['max_depth'], sub_analysis['max_depth'])
                                    analysis['arrays'] += sub_analysis['arrays']
                                    analysis['objects'] += sub_analysis['objects']
                                    
                                    for t, count in sub_analysis['types'].items():
                                        analysis['types'][t] = analysis['types'].get(t, 0) + count
                                else:
                                    value_type = type(item).__name__
                                    analysis['types'][value_type] = analysis['types'].get(value_type, 0) + 1
                        
                        return analysis
                    
                    analysis = analyze_json(parsed_json)
                    
                    col_stats1, col_stats2 = st.columns(2)
                    
                    with col_stats1:
                        st.metric("Total Keys", analysis['total_keys'])
                        st.metric("Max Depth", analysis['max_depth'])
                        st.metric("Objects", analysis['objects'])
                    
                    with col_stats2:
                        st.metric("Arrays", analysis['arrays'])
                        st.metric("Total Size", f"{len(formatted_json)} chars")
                        st.metric("Minified Size", f"{len(minified_json)} chars")
                    
                    if analysis['types']:
                        st.markdown("**Data Types:**")
                        for data_type, count in sorted(analysis['types'].items()):
                            st.text(f"• {data_type}: {count}")
                
                # Validation info
                st.success("✅ Valid JSON")
                
            except json.JSONDecodeError as e:
                st.error(f"❌ Invalid JSON: {str(e)}")
                
                # Try to show where the error is
                try:
                    error_line = str(e).split('line ')[1].split(' ')[0] if 'line ' in str(e) else None
                    if error_line:
                        st.error(f"Error appears to be around line {error_line}")
                except:
                    pass
                    
            except Exception as e:
                st.error(f"❌ Error processing JSON: {str(e)}")
        else:
            st.info("👈 Enter JSON on the left to format it")

# Footer with examples and tips
st.markdown("---")

with st.expander("📚 Examples & Tips"):
    tab1, tab2, tab3 = st.tabs(["String Examples", "Object Examples", "Pro Tips"])
    
    with tab1:
        st.markdown("**Common String Conversion Examples:**")
        
        examples = {
            "API Response": '{"status": "success", "message": "Hello World"}',
            "Multi-line Code": "function hello() {\n    console.log('Hello!');\n    return true;\n}",
            "Special Characters": 'Text with "quotes", \\backslashes\\ and \nnewlines',
            "Unicode Text": "Hello 世界! 🌍 Émojis and spëcial chars"
        }
        
        for name, example in examples.items():
            with st.container():
                st.markdown(f"**{name}:**")
                col_ex1, col_ex2 = st.columns([1, 1])
                
                with col_ex1:
                    st.text_area(
                        "Input:",
                        value=example,
                        height=80,
                        disabled=True,
                        key=f"ex_in_{name}"
                    )
                
                with col_ex2:
                    json_example = json.dumps(example, ensure_ascii=False)
                    st.code(json_example, language="json")
                    
                    if st.button(f"📋 Copy", key=f"copy_ex_{name}"):
                        copy_to_clipboard_js(json_example)
                        st.success("Copied!")
    
    with tab2:
        st.markdown("**JSON Object Building Examples:**")
        
        object_examples = {
            "User Profile": {
                "name": "John Doe",
                "age": 30,
                "active": True,
                "hobbies": ["reading", "coding", "gaming"],
                "address": {"city": "New York", "country": "USA"}
            },
            "API Configuration": {
                "endpoint": "https://api.example.com",
                "timeout": 5000,
                "retries": 3,
                "headers": {"Content-Type": "application/json"},
                "debug": False
            },
            "Product Data": {
                "id": "PROD-001",
                "name": "Wireless Headphones",
                "price": 99.99,
                "inStock": True,
                "categories": ["electronics", "audio"],
                "specs": {"battery": "20h", "weight": "250g"}
            }
        }
        
        for name, example in object_examples.items():
            with st.container():
                st.markdown(f"**{name}:**")
                formatted_example = json.dumps(example, indent=2, ensure_ascii=False)
                st.code(formatted_example, language="json")
                
                if st.button(f"📋 Copy {name}", key=f"copy_obj_ex_{name}"):
                    copy_to_clipboard_js(formatted_example)
                    st.success("Copied!")
    
    with tab3:
        st.markdown("**Pro Tips & Best Practices:**")
        
        tips = [
            "**String Converter**: Perfect for escaping text that contains quotes, backslashes, or newlines for use in JSON",
            "**Object Builder**: Build complex JSON objects step by step with validation",
            "**JSON Formatter**: Clean up and beautify messy JSON, with analysis tools",
            "**Import Feature**: Quickly load existing JSON into the Object Builder for editing",
            "**Copy Variations**: Use 'Copy for Code' to get properly escaped strings for programming",
            "**Validation**: All modes include real-time JSON validation with helpful error messages",
            "**File Support**: Upload text files, JSON files, or fetch content from URLs",
            "**Unicode Support**: Full support for international characters and emojis"
        ]
        
        for tip in tips:
            st.markdown(tip)
        
        st.markdown("---")
        st.markdown("**Keyboard Shortcuts:**")
        st.markdown("• `Ctrl/Cmd + A` to select all text in input areas")
        st.markdown("• `Ctrl/Cmd + C` to copy selected text")
        st.markdown("• Use the sidebar JSON validator for quick validation")

# Status bar
st.markdown("---")
col_status1, col_status2, col_status3 = st.columns(3)

with col_status1:
    st.markdown("**Current Mode:** " + mode)

with col_status2:
    if mode == "🗂️ JSON Object Builder":
        valid_pairs_count = sum(1 for pair in st.session_state.kv_pairs if pair["key"].strip())
        st.markdown(f"**Active Pairs:** {valid_pairs_count}")

with col_status3:
    st.markdown("**Status:** Ready ✅")

st.markdown(
    '<div style="text-align: center; color: #666; margin-top: 2rem;">'
    '💡 <strong>JSON Tool v2.0</strong> - Build, convert, and format JSON with ease!'
    '</div>',
    unsafe_allow_html=True
)