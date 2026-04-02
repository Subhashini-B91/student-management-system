import streamlit as st
import json

# ------------------ LOGIN ------------------
USERNAME = "admin"
PASSWORD = "1234"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == USERNAME and pwd == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.error("Invalid credentials")

if not st.session_state.logged_in:
    login()
    st.stop()
st.title("🎓 Student Management System")
# ------------------ DATA ------------------
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