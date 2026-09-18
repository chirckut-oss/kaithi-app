import streamlit as st
import sqlite3

# Page Configuration
st.set_page_config(page_title="Kaithi App", page_icon="📜", layout="centered")

# Database Connection Helper
def init_db():
    conn = sqlite3.connect('kaithi.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

st.title("📜 Kaithi App - Record Management")

# Sidebar for Navigation
menu = ["View Records", "Add Record", "Update Record"]
choice = st.sidebar.selectbox("Navigation", menu)

conn = sqlite3.connect('kaithi.db')
c = conn.cursor()

if choice == "Add Record":
    st.subheader("Add a New Record")
    with st.form("add_form"):
        title = st.text_input("Title")
        content = st.text_area("Content")
        submit_button = st.form_submit_button("Add Record")
        
        if submit_button:
            if title and content:
                c.execute("INSERT INTO records (title, content) VALUES (?, ?)", (title, content))
                conn.commit()
                st.success("Record added successfully!")
            else:
                st.warning("Please fill out both fields.")

elif choice == "View Records":
    st.subheader("All Records")
    c.execute("SELECT id, title, content FROM records")
    data = c.fetchall()
    
    if data:
        for row in data:
            st.write(f"**ID:** {row[0]} | **Title:** {row[1]}")
            st.write(f"**Content:** {row[2]}")
            st.markdown("---")
    else:
        st.info("No records found.")

elif choice == "Update Record":
    st.subheader("Update Existing Record")
    try:
        c.execute("SELECT id, title FROM records")
        records = c.fetchall()
        
        if records:
            record_dict = {f"{r[1]} (ID: {r[0]})": r[0] for r in records}
            selected_record_label = st.selectbox("Select Record to Update", list(record_dict.keys()))
            selected_id = record_dict[selected_record_label]
            
            # Fetch current content
            c.execute("SELECT title, content FROM records WHERE id = ?", (selected_id,))
            current_data = c.fetchone()
            
            with st.form("update_form"):
                new_title = st.text_input("Update Title", value=current_data[0])
                new_content = st.text_area("Update Content", value=current_data[1])
                update_button = st.form_submit_button("Update Record")
                
                if update_button:
                    c.execute("UPDATE records SET title = ?, content = ? WHERE id = ?", (new_title, new_content, selected_id))
                    conn.commit()
                    st.success(f"Record ID {selected_id} updated successfully!")
        else:
            st.info("No records available to update.")
            
    except Exception as e:
        st.error(f"An error occurred: {e}")

conn.close()
