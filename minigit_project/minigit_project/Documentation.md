# MiniGit Project Documentation

## Overview

MiniGit is a minimal version control system inspired by Git, implemented in Python as a command-line interface (CLI) tool. It allows users to initialize repositories, add files, commit changes, and view commit history, mimicking the basic workflow of Git. This documentation provides an overview of the data structures used, design decisions made, and limitations and future improvements for the project.

---

## Data Structures Used

### 1. `GitIndexEntry`
- **Purpose:** Represents an individual file entry in the staging area (index).
- **Attributes:**  
  - `ctime`, `mtime`: Creation and modification times (seconds/nanoseconds).
  - `dev`, `ino`: Device and inode numbers for file identity.
  - `mode_type`, `mode_perms`: File mode and permissions.
  - `uid`, `gid`: User and group IDs.
  - `fsize`: File size.
  - `sha`: Hash of the file contents (used to identify blob).
  - `flag_assume_valid`, `flag_stage`: Index flags.
  - `name`: File name (relative path).
- **Usage:** Used for tracking files added to the staging area before committing.

### 2. `GitIndex`
- **Purpose:** Represents the index (staging area) as a whole.
- **Attributes:**  
  - `version`: Index file version.
  - `entries`: List of `GitIndexEntry` objects.
- **Usage:** Read from and written to disk to represent the current staged state.

### 3. Commit Objects
- **Purpose:** Store a snapshot of the repository at a point in time.
- **Attributes:**
  - Tree SHA, parent commit(s), author info, timestamp, message.
- **Usage:** Written as files in the `.minigit/objects/` directory and referenced by SHA.

### 4. Trees and Blobs
- **Trees:** Represent directory structures, mapping filenames to blob (file) SHAs.
- **Blobs:** Store the content of individual files.
- **Usage:** Trees and blobs are serialized and referenced by SHA, recreating the repository state for each commit.

### 5. Other Data Structures
- **Dictionaries and Lists:** Used throughout for mapping names to objects, storing collections of commits, etc.

---

## Design Decisions

### 1. Git-like Directory Structure
- **Choice:** All repository data is stored in a hidden `.minigit` directory, closely mimicking the structure of a real Git repository.
- **Reason:** This allows for clear separation of version-controlled data from working files and prepares the codebase for potential future extension.

### 2. Modular Codebase
- **Choice:** Code is organized into modules: `cli.py` (command-line interface), `index.py` (staging/index logic), and `commands/` (individual command implementations).
- **Reason:** Improves maintainability, readability, and facilitates future development.

### 3. CLI Interface with Argparse
- **Choice:** The CLI is built using Python's `argparse` library to parse user commands.
- **Reason:** Provides a user-friendly interface and matches the usage pattern of the real Git CLI.

### 4. Cross-Platform Compatibility
- **Choice:** File operations and data serialization are written to work on both Windows and Unix-like systems.
- **Reason:** Ensures the tool is usable by all team members regardless of operating system.

### 5. Simplicity and Git Parity
- **Choice:** Only a core subset of Git features is implemented (`init`, `add`, `commit`, `status`, `log`, etc.).
- **Reason:** Focus on learning and clear demonstration of core version control concepts.

---

## Limitations and Future Improvements

### **Current Limitations**
- **Limited Feature Set:** Only basic commands are supported (no branching, merging, remotes, or conflict resolution).
- **No Remote Support:** Cannot push to or pull from remote repositories.
- **No File Deletion Tracking:** Deleted files are not properly tracked in commits.
- **No Merge or Branching:** Features like branching, merging, and tags are absent.
- **No Binary File Handling:** Project is primarily tested with text files; binary file support is not guaranteed.
- **Minimal Error Handling:** Edge cases and error handling are basic; user feedback can be improved.

### **Future Improvements**
- **Implement Branching and Merging:** Add support for branches and merge operations, including conflict resolution.
- **Remote Repository Support:** Enable pushing to and pulling from remote repositories.
- **File Deletion and Rename Tracking:** Accurately track deleted and renamed files.
- **Improve CLI and Help Messages:** Provide better user guidance and error messages.
- **Add Test Suite:** Develop automated tests for all major features.
- **Performance Optimization:** Refactor code to efficiently handle large repositories and files.
- **User Authentication and Access Control:** For remote features, add authentication mechanisms.
- **Expand Documentation:** Provide user guides, developer docs, and more code comments.

---

## Conclusion

MiniGit demonstrates the foundational concepts of version control systems, including staging, committing, and history traversal. The project is designed for learning and extensibility, with a modular codebase and a Git-inspired structure. While limited in scope compared to full-featured systems, it provides a strong foundation for further exploration and development.
