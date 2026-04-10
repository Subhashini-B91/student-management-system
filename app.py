import streamlit as st
import json
# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)

# ------------------ CUSTOM HEADER ------------------
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>
    🎓 Student Management System
    </h1>
    <hr style='border: 1px solid #ddd;'>
""", unsafe_allow_html=True)
# ------------------ BACKGROUND STYLE ------------------
st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(to right, #e3f2fd, #ffffff);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #f0f8ff;
}

/* Card-like sections */
.block-container {
    padding: 2rem;
    border-radius: 10px;
}

/* Buttons */
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
}

/* Input fields */
.stTextInput>div>div>input {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* Make all text green */
html, body, [class*="css"]  {
    color: #2e7d32 !important;
}

/* Headings */
h1, h2, h3, h4 {
    color: #2e7d32 !important;
}

/* Labels and input text */
label, .stTextInput, .stNumberInput {
    color: #2e7d32 !important;
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: #2e7d32 !important;
}

/* Buttons text */
.stButton>button {
    color: white !important;
    background-color: #2e7d32 !important;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* Selectbox (dropdown menu text) */
div[data-baseweb="select"] * {
    color: #2e7d32 !important;
}

/* Selected value inside selectbox */
div[data-baseweb="select"] span {
    color: #2e7d32 !important;
}

/* Dropdown options */
ul[role="listbox"] li {
    color: #2e7d32 !important;
}

/* Radio buttons (if you use them) */
div[role="radiogroup"] label {
    color: #2e7d32 !important;
}

/* Sidebar selectbox specifically */
[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #2e7d32 !important;
}

</style>
""", unsafe_allow_html=True)
def load_data():
    try:
        with open("students.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open("students.json", "w") as f:
        json.dump(data, f)

def calculate_grade(marks):
    avg = sum(marks) / len(marks)
    if avg >= 90:
        return "A"
    elif avg >= 75:
        return "B"
    elif avg >= 50:
        return "C"
    else:
        return "F"

students = load_data()

# ------------------ UI ------------------
choice = st.radio(
    "Select Option",
    ["Add", "View", "Search", "Update", "Delete"],
    horizontal=True
)
# ------------------ ADD ------------------
if choice == "Add":
    st.subheader("➕ Add Student")

    roll = st.text_input("Roll No")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    course = st.text_input("Course")
    marks = st.text_input("Marks (comma separated)")

    if st.button("Add Student"):
        marks_list = list(map(int, marks.split(",")))
        grade = calculate_grade(marks_list)

        students.append({
            "roll_no": roll,
            "name": name,
            "age": age,
            "course": course,
            "marks": marks_list,
            "grade": grade
        })

        save_data(students)
        st.success("✅ Student Added")

# ------------------ VIEW ------------------
elif choice == "View":
    st.subheader("📋 Student Records")

    if students:
        st.dataframe(students)
    else:
        st.warning("No records found")

# ------------------ SEARCH ------------------
elif choice == "Search":
    st.subheader("🔍 Search Student")

    roll = st.text_input("Enter Roll No")

    if st.button("Search"):
        for s in students:
            if s["roll_no"] == roll:
                st.success("Student Found")
                st.json(s)
                break
        else:
            st.error("Student not found")

# ------------------ UPDATE ------------------
elif choice == "Update":
    st.subheader("✏️ Update Student")

    roll = st.text_input("Enter Roll No")

    for s in students:
        if s["roll_no"] == roll:
            name = st.text_input("Name", s["name"])
            course = st.text_input("Course", s["course"])
            marks = st.text_input("Marks", ",".join(map(str, s["marks"])))

            if st.button("Update"):
                marks_list = list(map(int, marks.split(",")))
                s["name"] = name
                s["course"] = course
                s["marks"] = marks_list
                s["grade"] = calculate_grade(marks_list)

                save_data(students)
                st.success("Updated Successfully")
            break

# ------------------ DELETE ------------------
elif choice == "Delete":
    st.subheader("🗑 Delete Student")

    roll = st.text_input("Enter Roll No")

    if st.button("Delete"):
        new_data = [s for s in students if s["roll_no"] != roll]

        if len(new_data) != len(students):
            save_data(new_data)
            st.success("Deleted Successfully")
        else:
            st.error("Student not found")
