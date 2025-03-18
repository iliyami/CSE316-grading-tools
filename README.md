# **📌 Grading Setup Automation Script**

```
    ░▒▓██████▓▒░ ░▒▓███████▓▒░▒▓████████▓▒░      ░▒▓███████▓▒░   ░▒▓█▓▒░░▒▓███████▓▒░ 
    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░                    ░▒▓█▓▒░▒▓████▓▒░▒▓█▓▒░        
    ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░                    ░▒▓█▓▒░  ░▒▓█▓▒░▒▓█▓▒░        
    ░▒▓█▓▒░       ░▒▓██████▓▒░░▒▓██████▓▒░        ░▒▓███████▓▒░   ░▒▓█▓▒░▒▓███████▓▒░  
    ░▒▓█▓▒░             ░▒▓█▓▒░▒▓█▓▒░                    ░▒▓█▓▒░  ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░                    ░▒▓█▓▒░  ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░      ░▒▓███████▓▒░   ░▒▓█▓▒░░▒▓██████▓▒░  
                                                                                   
                            GitHub Repository Grading Automation  
                            👨‍💻 **Created by: Iliya Mirzaei**  
```

## **🔹 Overview**
This script automates the **grading setup** for student repositories in **CSE316** by:  
✅ **Cloning GitHub repositories** using SSH  
✅ **Copying grading templates** into each repository  
✅ **Preserving Excel formatting** while filling in team & student details  
✅ **Extracting commit timestamps** to assess late submissions  
✅ **Applying automatic penalties** based on a **configurable deadline policy**  
✅ **Handling deadline extensions** for specific teams  
✅ **Skipping commits** only for deadline calculations  
✅ **Logging late submissions** in a dedicated `late_submissions.txt` file  

---

## **📥 Installation**
1. **Install Python 3.7+** (if not already installed).  
2. Install dependencies using:  
   ```sh
   pip install -r requirements.txt
   ```
3. Ensure your **SSH key is added to GitHub**:  
   ```sh
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   ssh-add ~/.ssh/id_rsa
   ssh -T git@github.com
   ```
📌 **Important:** After generating your SSH key, you must add it to your **GitHub account** manually.  
🔗 **GitHub SSH Key Setup Guide:** [Adding a new SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)  


---

## **🚀 Usage**
Run the script with:  
```sh
python script.py "<Grader Name>" "<test_file.xlsx>" "<team_grading.xlsx>" "<Deadline MM-DD-YYYY>" [Grace Period (default: 0 hours)] [Skip Commits]
```

### **🔹 Arguments**
| Argument | Description |
|----------|------------|
| `<Grader Name>` | The name of the grader (used for filtering). |
| `<test_file.xlsx>` | Path to the test grading template file. |
| `<team_grading.xlsx>` | Path to the file containing student repositories and assignments. |
| `<Deadline MM-DD-YYYY>` | The **official** submission deadline for grading. |
| `[Grace Period]` (optional) | Extra hours (default: **0 hours**) where late penalties **do not apply**. |
| `[extension_file.txt]` (optional) | Path to a file containing team-specific deadline extensions. |
| `[Skip Commits]` (optional) | **Number of commits to skip when calculating the deadline** (default: 0). |

---

## **📑 File Formats**
### **1️⃣ Team Grading File (`team_grading.xlsx`)**
Must contain the following **columns**:

| Column Name | Description |
|-------------|------------|
| **group_name** | The team name or project group. |
| **Grader Name** | The assigned grader's name. |
| **Grader Email** | The grader’s email address. |
| **roster_identifier** | The student’s email in `x_y.z@q.d` format (used for name extraction). |
| **student_repository_url** | The **HTTP** GitHub repository URL (converted to SSH). |

---

### **2️⃣ Test File (`test_file.xlsx`)**
This **grading template** must contain the following placeholders in the first column:

| Column 1 (Title) | Column 2 (Filled by Script) |
|------------------|---------------------------|
| **Team Name:** | (Auto-filled) |
| **Student 1:** | (Auto-filled) |
| **Student 2:** | (Auto-filled) |
| **Grader Name:** | (Auto-filled) |
| **Grader Email:** | (Auto-filled) |

> 📌 **The script fills these values while preserving Excel formatting.**  

---

### **3️⃣ Deadline Extension File (`extension_file.txt`)** _(Optional)_
This file specifies **team-specific deadline extensions** in the following format:

```
Student 1 & Student 2 - My Team, 03/09/2025
```
- The **first part** (`Student 1 & Student 2`) is **for reference only**.  
- The **team name** (`My Team`) **must match** the `group_name` from `team_grading.xlsx`.  
- The **new deadline** (`03/09/2025`) is applied **instead of the original** deadline.

---

## **📊 Late Submission Policy**
🚨 **Penalties are applied based on the last commit timestamp:**  
- **⏳ On time** → **No penalty** (submitted within `[grace period]` after the deadline).  
- **Late (6-30 hours)** → **Max Score: 90%**  
- **Late (30-54 hours)** → **Max Score: 80%**  
- **Late (54-78 hours)** → **Max Score: 70%**  
- **Late (78-102 hours)** → **Max Score: 60%**  
- **Late (102+ hours)** → **Max Score: 50%**  

> 📝 **If a team has an extension,** the **effective deadline** is updated before penalties are applied.

---

---

## **🔄 Skipping Commits for Deadline Calculations**
- **The script always clones the latest commit** from the repository.  
- **However, for submission time calculations**, it checks an earlier commit by skipping `X` commits (if specified).  

📌 **Example:**  
If the last **4 commits** were:  
```
Commit A (Latest)  →  March 10, 2025
Commit B           →  March 9, 2025
Commit C           →  March 8, 2025
Commit D           →  March 7, 2025
```
Running:
```sh
python script.py "John Doe" "grading_template.xlsx" "team_grading.xlsx" "03-06-2025" 6 "Extensions.txt" 2
```
- The script **clones the latest commit (A)**
- But **uses Commit C's timestamp (March 8) for deadline penalties**.  

---

## **📂 Late Submission Log (`late_submissions.txt`)**
All late submissions are logged in **`late_submissions.txt`**, including:

✅ **Team Name**  
✅ **Submission Timestamp**  
✅ **Original Deadline & Extension Deadline (if any)**  
✅ **Time Difference from Deadline**  
✅ **Final Submission Status & Score Cap**  

### **📜 Example Log:**
```
📌 Late Submissions Log
--------------------
Team: My Team
   - 🕒 Submission Timestamp: 2025-03-09 15:54:20
   - 📝 Original Deadline: 2025-03-06 00:00:00
   - ⏳ Time Difference: 15.91 hours
   - 🚦 Submission Status: ⏳ Late (90% cap)
   - 🆓 Extension Granted Until: 2025-03-09 00:00:00
   - 🔴 Max Score Capped at 90%
```

---

## **📌 Example Run**
```sh
python grading_script.py "Iliya Mirzaei" "grading_template.xlsx" "team_grading.xlsx" "03-06-2025" 6 "extensions.txt"
```

### **🔹 What Happens?**
✅ Filters teams assigned to **Iliya Mirzaei** TA(Grader)   
✅ Clones **each team's repository**  
✅ Copies and fills in **grading templates**  
✅ Extracts **last commit timestamps**  
✅ Applies **late penalties (if any)**  
✅ Logs **all late submissions** in `late_submissions.txt`  

---

## **🛠️ Troubleshooting**
### **🔹 1. GitHub SSH Key Not Working?**
Ensure you've **added your SSH key to your GitHub account**:  
🔗 **GitHub SSH Key Setup Guide:** [Adding a new SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

---

### **🔹 2. `ssh-add` Fails? (SSH-Agent Not Running)**
If `ssh-add` fails, it may be because the **SSH-agent** is not running.  
🔗 **How to Fix:** [Start the SSH-agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/working-with-ssh-key-passphrases#start-the-ssh-agent)

---

### **🔹 Missing Dependencies?**
```sh
pip install -r requirements.txt
```

---

## **👨‍💻 Contributing**
Feel free to **open an issue** or **submit a pull request** for improvements!  

---

## **📜 License**
This script is **open-source** under the **MIT License**.

---