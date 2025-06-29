# WV-HOT-WORD for Notepad++
**A Swiss Army Knife for Symbol-Based Navigation**  
*(.classes, #definitions, >search, etc.)*

---

## ❓ Help Wanted  
- [ ] Document the code (I'm dyslexic).  
- [ ] Add new ideas and suggestions.  
- [ ] Test on different systems.

> **Contact**: [Your email/Discord here]

---

## 🚀 Key Features
- **Smart Search**:
  - `.myClass` → Finds class declarations  
  - `#define` → Finds definitions  
  - `>word` → Iterative search
- **Navigation**:
  - ` ` (space) → Go back to previous position  
  - `*term` → Search in glossary
- **Project Management**:
  - Position history (`Alt+W` to navigate)  
  - Multi-file support

---

## 📦 File Structure

| File               | Purpose                                                              |
|--------------------|----------------------------------------------------------------------|
| `WvJsBasic.py`     | Main entry point                                                     |
| `editor_.py`       | Interface with Notepad++ (cursor, selections, etc.)                  |
| `hot_commands.py`  | Command dictionary (`#help`, `>search`, etc.)                        |
| `hot_goto.py`      | Handles jumps and position-based searches                            |
| `hot_parser.py`    | Parses symbol-based triggers (`.`, `#`, `>`)                         |
| `project_.py`      | Project initialization and dependency management                     |

---

## 🛠 Installation
1. Copy all files into `plugins/PythonScript/scripts/` in your Notepad++ folder  
2. Launch `WvJsBasic.py` via *PythonScript* > *Run...*  
3. In an open file in Notepad++, add symbols around words and press Alt-W

---

## 🎯 Usage Examples
```python
# Find a class
.myClass  # → Jumps to the "class myClass" declaration

# Find a definition
#setup     # → Finds "def setup()"

# Navigate
myWord >   # → Searches for "myWord" across all open files
```
