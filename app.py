import streamlit as st
import pandas as pd
import numpy as np 
import cleaning as cl
import temp as tp
import io

# THIS FUNCTION VALIDATE THE LOADED DATA 
def load_data(file):
    if file is None:
        print("File is empty or missing")
        return None
    
    data = pd.read_csv(file)

    if data.empty:
        print("DataFrame is empty")
        return None
    else :
        return data

#THIS IS THE UPLOADER PAGE
def upload_page():
    st.markdown("---")
    st.markdown("# 🧼 Data Cleaner")
    st.markdown("##### Upload your CSV file and we'll help you clean it up")
    st.markdown("---")

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        file = st.file_uploader("📂 Drop your CSV file here", type=["csv"])
        data = load_data(file)

        if file:
            st.success(f"✅ **{file.name}** uploaded successfully!")

        st.markdown("")
        inspect = st.button("🔍 Inspect & Start Cleaning", use_container_width=True, type="primary")
        if inspect:
            if data is None:
                st.warning("⚠️ Please upload a valid CSV file before inspecting.")
                return data
            st.session_state.page = 1
            st.session_state.data = data
            st.rerun()

    return data

#THIS PAGE IS FOR INSPECTING THE DATA
def inspect_page(data):
    st.subheader("Overview")
    shape=data.shape
    size_mb = round(data.size / (1024 * 1024), 2)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", shape[0])
    with col2:
        st.metric("Columns", shape[1])
    with col3:
        st.metric("File Size", f"{size_mb} MB")
        
    st.divider()
    
    st.subheader("Column Info")
    st.session_state.cols = data.dtypes
    st.dataframe(st.session_state.cols.astype(str))
    
    st.divider()
    
    st.subheader("Missing Values")
    st.session_state.nan_value = data.isna().sum()
    st.dataframe(st.session_state.nan_value)
    
    st.divider()

    st.subheader("Duplicates")
    duplicated = (data.duplicated()).sum()
    if duplicated == 0:
        st.success("No duplicate rows found")
    else:
        st.warning(f"{duplicated} duplicate rows found")
    
    st.divider()
    
    st.subheader("Statistical summary ")
    st.session_state.stat_summry=data.describe()
    st.dataframe(st.session_state.stat_summry)
    
    st.divider()
    
    st.subheader("Table overview")
    overview=pd.concat([data.head(5), data.tail(5)])
    st.dataframe(overview)
    b1,b2= st.columns(2)
    with b1:
        st.markdown("#### ✏️ Rename Columns")
        st.markdown("Want to rename any of your column headers?")
        if st.button("Yes, rename columns", use_container_width=True, type="primary"):
            st.session_state.page = 2
            st.rerun()

    with b2:
        st.markdown("#### ⏭️ Skip")
        st.markdown("Happy with your column names as they are?")
        if st.button("No, skip to cleaning", use_container_width=True):
            st.session_state.page = 3
            st.rerun()
  
# THIS FUNCTION MODIFYS THE NAME OF THE DATA SET 
def column_name_modification(data):
    if "new_page" not in st.session_state:
        st.session_state.new_page = False
    if "pass_data" not in st.session_state:
        st.session_state.pass_data = data
    if "old_name" not in st.session_state:
        st.session_state.old_name = st.session_state.pass_data.columns.tolist()
    if 'i' not in st.session_state:
        st.session_state.i = 0
        st.session_state.new_column = []

    old_name = st.session_state.old_name  # always pulled from session state

    if st.session_state.i == len(old_name):
        st.session_state.pass_data.columns = st.session_state.new_column
        return st.session_state.pass_data, True

    if "button2" not in st.session_state:
        st.session_state.button2 = False

    st.markdown("---")
    st.caption(f"Column {st.session_state.i + 1} of {len(old_name)}")
    st.progress(st.session_state.i / len(old_name))
    st.markdown(f"### 🏷️ `{old_name[st.session_state.i]}`")
    st.info("✏️ Keep the column name as is, or rename it below")
    st.markdown("---")

    col1, col2 = st.columns([1, 2])
    with col1:
        button1 = st.button("✅ Keep", key=f"n{old_name[st.session_state.i]}", use_container_width=True)
    if button1:
        st.session_state.new_column.append(old_name[st.session_state.i])
        st.session_state.i += 1
        st.rerun()
    with col2:
        st.session_state.new_name = st.text_input("New name:", placeholder="Enter new column name...", key=f"name_input_{st.session_state.i}")
        done = st.button("✅ Enter", use_container_width=True)
    if done:
        st.session_state.new_column.append(st.session_state.new_name)
        st.session_state.i += 1
        st.rerun()

    st.dataframe(st.session_state.pass_data)
    return st.session_state.pass_data, False  # always return two values
 

#THIS FUNCTION MODIFY THE DATATYPE OF THE TABLE
def columns_datatype(data):
    if "new_page" not in st.session_state:
        st.session_state.new_page = False
    if "pass_data" not in st.session_state:
        st.session_state.pass_data = data
    st.title("🧹 Data Cleaning Tool")
    st.divider()
    st.session_state.name=st.session_state.pass_data.columns
    choice=None
    if 'i' not in st.session_state:
        st.session_state.i=0
    if st.session_state.i==len(st.session_state.name):
        return st.session_state.pass_data, True 
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Column {st.session_state.i + 1} of {len(st.session_state.name)}")
        st.info(f"**Column name:** `{st.session_state.name[st.session_state.i]}`")
        choice = st.radio(
            "What is the data type of this column?",
            ["integer", "string", "datetime", "boolean"],
            key=(st.session_state.name[st.session_state.i]),index=None
        )
        Enter = st.button("Enter ➡️")
    if Enter:
        if choice=="integer":
            st.session_state.pass_data [st.session_state.name[st.session_state.i]]=pd.to_numeric(st.session_state.pass_data [st.session_state.name[st.session_state.i]],errors="coerce")
        elif choice=="string":
            st.session_state.pass_data [st.session_state.name[st.session_state.i]]=st.session_state.pass_data [st.session_state.name[st.session_state.i]].astype(str)
        elif choice=="datetime":
            st.session_state.pass_data [st.session_state.name[st.session_state.i]] = pd.to_datetime(st.session_state.pass_data [st.session_state.name[st.session_state.i]], errors="coerce")
        elif choice=="boolean":
            st.session_state.pass_data [st.session_state.name[st.session_state.i]]=st.session_state.pass_data [st.session_state.name[st.session_state.i]].astype(bool) 
        st.session_state.i+=1
        
        if st.session_state.i==len(st.session_state.name):
            st.session_state.page+=1
        st.rerun()
    with col2:
        st.metric("Progress", f"{st.session_state.i}/{len(st.session_state.name)}")
        st.progress(st.session_state.i / len(st.session_state.name))
    st.dataframe(st.session_state.pass_data)
    return st.session_state.pass_data, False 
        
#THIS FUNCTION HANDLES MISSING DATAS IN THE TABLE            
def missing_values(data):
    if "pass_data" not in st.session_state:
        st.session_state.pass_data = data
    if "name" not in st.session_state:
        st.session_state.name = st.session_state.pass_data.columns
    if 'i' not in st.session_state:
        st.session_state.i = 0
        st.session_state.pass_data = st.session_state.pass_data.drop_duplicates()
        st.session_state.pass_data = st.session_state.pass_data.replace(
        ["", " ", "  ", "NA", "N/A", "na", "n/a", "NaN", "nan", "NULL", "null",
         "None", "none", "-", "--", "---", "_", "?", "missing", "Missing", "MISSING",
         "unknown", "Unknown", "UNKNOWN", "not available", "Not Available",
         "not applicable", "Not Applicable", "#N/A", "#VALUE!", "#NULL!"], np.nan)

    if st.session_state.i == len(st.session_state.name):
        return st.session_state.pass_data, True 

    # ── Header ──────────────────────────────────────────
    st.title("🧹 Missing Values Handler")
    st.divider()

    # ── Progress ─────────────────────────────────────────
    progress = st.session_state.i / len(st.session_state.name)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(progress)
    with col2:
        st.metric("Progress", f"{st.session_state.i}/{len(st.session_state.name)}")

    st.divider()

    # ── Column Info ───────────────────────────────────────
    current_col = st.session_state.name[st.session_state.i]
    missing_count = st.session_state.pass_data[current_col].isna().sum()
    total_count = len(st.session_state.pass_data)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Column**\n\n`{current_col}`")
    with col2:
        st.warning(f"**Missing Values**\n\n{missing_count}")
    with col3:
        st.metric("Missing %", f"{round((missing_count / total_count) * 100, 1)}%")

    st.divider()

    # ── Choice ────────────────────────────────────────────
    st.subheader("How do you want to handle missing values?")

    options = {
        1: "🗑️ Drop rows with missing values",
        2: "0️⃣  Fill with 0",
        3: "📊 Fill with Mean",
        4: "📈 Fill with Median",
        5: "🔢 Fill with Mode",
    }

    st.session_state.choice = st.radio(
        "Select strategy:",
        options=list(options.keys()),
        format_func=lambda x: options[x],
        key=current_col,
        index=None,
    )

    st.divider()
    enter = st.button("Enter ➡️", use_container_width=True)

    if enter:
        if st.session_state.choice == 1:
            st.session_state.pass_data = st.session_state.pass_data.dropna(subset=[current_col])
        elif st.session_state.choice == 2:
            st.session_state.pass_data[current_col] = st.session_state.pass_data[current_col].fillna(0)
        elif st.session_state.choice == 3:
            st.session_state.pass_data[current_col] = st.session_state.pass_data[current_col].fillna(st.session_state.pass_data[current_col].mean())
        elif st.session_state.choice == 4:
            st.session_state.pass_data[current_col] = st.session_state.pass_data[current_col].fillna(st.session_state.pass_data[current_col].median())
        elif st.session_state.choice == 5:
            st.session_state.pass_data[current_col] = st.session_state.pass_data[current_col].fillna(st.session_state.pass_data[current_col].mode()[0])
        st.session_state.i += 1
        st.rerun()
    
    return st.session_state.pass_data, False

# THIS FUNCTION MODFYS STRINGS OF THE TABLE LIKE CAPITALIZE REMOVE WHITE SPACE       
def Clean_text_data(data):
    if "pass_data" not in st.session_state:
        st.session_state.pass_data = data
    if "name" not in st.session_state:
        st.session_state.name = st.session_state.pass_data.columns
    if 'i' not in st.session_state:
        st.session_state.last_action=None
        st.session_state.i = 0
    if st.session_state.i == len(st.session_state.name):
        return st.session_state.pass_data, True 

    st.markdown("---")
    st.markdown(f"### 🧹 Cleaning Column: `{st.session_state.name[st.session_state.i]}`")
    st.markdown(f"**{st.session_state.i + 1}** of **{len(st.session_state.name)}** columns")
    st.markdown("---")
    if st.session_state.last_action:
        st.success(st.session_state.last_action)

    st.session_state.col_name = st.session_state.name[st.session_state.i]

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### ✂️ Whitespace")
        if st.button("Strip edges", use_container_width=True):
            st.session_state.pass_data[st.session_state.col_name] = st.session_state.pass_data[st.session_state.col_name].str.strip()
            st.session_state.last_action = "✅ Edges stripped!"
            st.rerun()
        if st.button("Remove all spaces", use_container_width=True):
            st.session_state.pass_data[st.session_state.col_name] = st.session_state.pass_data[st.session_state.col_name].str.replace(" ", "")
            st.session_state.last_action = "✅ All spaces removed!"
            st.rerun()

    with c2:
        st.markdown("#### 🔡 Casing")
        if st.button("UPPERCASE", use_container_width=True):
            st.session_state.pass_data[st.session_state.col_name] = st.session_state.pass_data[st.session_state.col_name].str.upper()
            st.session_state.last_action = "✅ Converted to UPPERCASE!"
            st.rerun()
        if st.button("lowercase", use_container_width=True):
            st.session_state.pass_data[st.session_state.col_name] = st.session_state.pass_data[st.session_state.col_name].str.lower()
            st.session_state.last_action = "✅ Converted to lowercase!"
            st.rerun()
        if st.button("Capitalize first", use_container_width=True):
            st.session_state.pass_data[st.session_state.col_name] = st.session_state.pass_data[st.session_state.col_name].str.capitalize()
            st.session_state.last_action = "✅ First letter capitalized!"
            st.rerun()

    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Next column ➡️", use_container_width=True):
            st.session_state.i += 1
            st.session_state.last_action = ""
            st.rerun()
    return st.session_state.pass_data, False

def download_page(data):
    if "pass_data" not in st.session_state:
        st.session_state.pass_data = data

    st.markdown("---")
    st.markdown("## 🎉 Your data is clean and ready!")
    st.markdown("---")

    # stats
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Rows", st.session_state.pass_data.shape[0])
    with c2:
        st.metric("Columns", st.session_state.pass_data.shape[1])
    with c3:
        st.metric("Total Cells", st.session_state.pass_data.shape[0] * st.session_state.pass_data.shape[1])

    st.markdown("---")
    st.markdown("### 👀 Preview")
    st.dataframe(st.session_state.pass_data, use_container_width=True)

    st.markdown("---")
    st.markdown("### 💾 Download")

    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            label="⬇️ Download as CSV",
            data=st.session_state.pass_data.to_csv(index=False),
            file_name="cleaned_data.csv",
            mime="text/csv",
            use_container_width=True
        )
    with c2:
        buffer = io.BytesIO()
        st.session_state.pass_data.to_excel(buffer, index=False, engine="openpyxl")
        st.download_button(
            label="⬇️ Download as Excel",
            data=buffer.getvalue(),
            file_name="cleaned_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    

    
    
        
    

    
def main():
    if "page" not in st.session_state:
        st.session_state.page=0
    if st.session_state.page==0: 
        st.session_state.data=upload_page()
    elif st.session_state.page==1: 
        inspect_page(st.session_state.data)
    elif st.session_state.page == 2:
        st.session_state.data, next_page = column_name_modification(st.session_state.data)
        if next_page:
            st.session_state.page = 3
            del st.session_state['i']
            st.rerun()
    elif st.session_state.page==3:
        st.session_state.data, next_page1=columns_datatype(st.session_state.data)
        if next_page1:
            st.session_state.page = 4
            del st.session_state['i']
            st.rerun()
    elif st.session_state.page == 4:
        st.session_state.data, next_page2 = missing_values(st.session_state.data)
        if next_page2:
            st.session_state.page = 5
            del st.session_state['i']
            st.rerun()

    elif st.session_state.page == 5:
        st.session_state.data, next_page3 = Clean_text_data(st.session_state.data)
        if next_page3:
            st.session_state.page = 6
            del st.session_state['i']
            st.rerun()
    elif st.session_state.page==6:
        st.session_state.data, next_page3 = missing_values(st.session_state.data)
        if next_page3:
            st.session_state.page = 7
            del st.session_state['i']
            st.rerun()
    elif st.session_state.page==7:
        download_page(st.session_state.data)
           
        
         

if __name__ == "__main__":
    main()
    


  
  
  

  
  
  
  
  
  
  
  
 





