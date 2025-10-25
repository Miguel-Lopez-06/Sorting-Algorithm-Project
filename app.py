import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")

# --- Sidebar Layout (pure Streamlit, left-aligned) ---
st.markdown("""
    <style>
    .nav-button-uniform button {
        width: 100% !important;
        min-width: 210px !important;
        max-width: 210px !important;
        margin-bottom: 12px !important;
        border-radius: 10px !important;
        border: 1.5px solid #444857 !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        text-align: center !important;
        align-items: center !important;
        justify-content: center !important;
        padding-top: 0.5em !important;
        padding-bottom: 0.5em !important;
        background: none !important;
        color: #e3e6f3 !important;
        white-space: normal !important;
        word-break: break-word !important;
        display: flex !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Layout (left-aligned and uniform width) ---
with st.sidebar:
    st.markdown("## Sorting Algorithm Interpreter Project")
    st.write("")
    st.write("Pages")
    if "page" not in st.session_state:
        st.session_state.page = "Home Page"
    # Uniform width nav buttons (with Streamlit 1.23+)
    col = st.container()
    with col:
        if st.button("Home Page", key="home", help=None, type="secondary", use_container_width=True):
            st.session_state.page = "Home Page"
        if st.button("Project Details", key="proj", help=None, type="secondary", use_container_width=True):
            st.session_state.page = "Details"
        if st.button("Sorting Algorithm Interpreter", key="viz", help=None, type="secondary", use_container_width=True):
            st.session_state.page = "Visualization"
    st.markdown("---")
    st.write("Abstract")
    st.markdown(
        "A Streamlit dashboard for visually comparing four classic sorting algorithms "
        "(Bubble, Insertion, Quick, Merge) using a custom interpreter engine with live step-by-step output."
    )
    st.markdown("---")
    st.write("Links:")
    st.markdown(
        "[Github Repository](https://github.com/Miguel-Lopez-06/Sorting-Algorithm-Project.git)"
    )
    st.markdown(
        "[Google Colab Notebook](https://colab.research.google.com/drive/1ILGTrV-2Jzcif9-kHgX4eCTh-5_5kPhB?usp=sharing)"
    )
    st.markdown("---")
    st.write("Group: Torpezoids")
    st.write("Members:")
    st.write("Lopez, Miguel")
    st.write("Mirabel, Jan Kristian")
    st.write("Sobrepena, Kim")

# --- Sorting & Visualization Functions ---
def get_color_dict(values):
    sorted_vals = sorted(set(values), key=lambda x: (isinstance(x, int), x))
    color_list = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'yellow', 'gray', 'cyan']
    color_dict = {val: color_list[i % len(color_list)] for i, val in enumerate(sorted_vals)}
    return color_dict

def bubble_sort_history(arr, order):
    arr = arr[:]
    history = [arr[:]]
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if (order == 'ASC' and arr[j] > arr[j + 1]) or (order == 'DESC' and arr[j] < arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                history.append(arr[:])
    return history

def insertion_sort_history(arr, order):
    arr = arr[:]
    history = [arr[:]]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and ((order == 'ASC' and arr[j] > key) or (order == 'DESC' and arr[j] < key)):
            arr[j + 1] = arr[j]
            j -= 1
            history.append(arr[:])
        arr[j + 1] = key
        history.append(arr[:])
    return history

def quick_sort_history(arr, order):
    history = []
    def _quick_sort(a, l, r):
        if l < r:
            pi = partition(a, l, r)
            _quick_sort(a, l, pi - 1)
            _quick_sort(a, pi + 1, r)
    def partition(a, l, r):
        pivot = a[r]
        i = l - 1
        for j in range(l, r):
            if (order == 'ASC' and a[j] < pivot) or (order == 'DESC' and a[j] > pivot):
                i += 1
                if i != j:
                    a[i], a[j] = a[j], a[i]
                    history.append(a[:])
        if i + 1 != r:
            a[i + 1], a[r] = a[r], a[i + 1]
            history.append(a[:])
        return i + 1
    a = arr[:]
    history.append(a[:])
    _quick_sort(a, 0, len(a) - 1)
    return history

def merge_sort_history(arr, order):
    history = []
    def _merge_sort(a, l, r):
        if l < r:
            m = (l + r) // 2
            _merge_sort(a, l, m)
            _merge_sort(a, m + 1, r)
            merge(a, l, m, r)
    def merge(a, l, m, r):
        left = a[l:m+1]
        right = a[m+1:r+1]
        i = j = 0
        for k in range(l, r + 1):
            if i < len(left) and (j == len(right) or
               ((order == 'ASC' and left[i] <= right[j]) or (order == 'DESC' and left[i] >= right[j]))):
                a[k] = left[i]
                i += 1
            else:
                a[k] = right[j]
                j += 1
            history.append(a[:])
    a = arr[:]
    history.append(a[:])
    _merge_sort(a, 0, len(a) - 1)
    return history

def plot_legend_bar(values, color_dict):
    fig, ax = plt.subplots(figsize=(len(values), 0.5))
    for i, val in enumerate(values):
        ax.barh(0, 1, left=i, color=color_dict[val], edgecolor='black')
        ax.text(i + 0.5, 0, str(val), ha='center', va='center', color='white', fontsize=12)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_xlim(0, len(values))
    ax.set_title('Legend: Value-Color Mapping', fontsize=12)
    plt.box(False)
    plt.tight_layout()
    return fig

def plot_history_grid(history, color_dict, order_choice):
    num_steps = len(history)
    ncols = 3
    nrows = (num_steps + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(12, 3 * nrows))
    axes = np.array(axes).reshape(-1, ncols)
    for idx, step in enumerate(history):
        row = idx // ncols
        col = idx % ncols
        ax = axes[row, col] if nrows > 1 else axes[col]
        bar_colors = [color_dict[v] for v in step]
        ax.bar(range(len(step)), step, color=bar_colors)
        ax.set_title(f"Step {idx}")
        label_text = f"{'Ascending' if order_choice == 'ASC' else 'Descending'} Order"
        ax.set_xlabel(label_text)
        ax.set_ylabel('Value')
        ax.set_ylim(0, max(max(s) for s in history) + 1)
        ax.set_xticks(range(len(step)))
        ax.set_xticklabels([str(x) for x in range(len(step))])
    for j in range(num_steps, nrows * ncols):
        row = j // ncols
        col = j % ncols
        ax = axes[row, col] if nrows > 1 else axes[col]
        ax.axis('off')
    plt.tight_layout()
    return fig

# --- Main Page Routing ---
if st.session_state.page == "Home Page":
    st.title("Sorting Algorithm Interpreter Project")
    st.markdown("""
    ### Project Introduction
    This project implements a **Sorting Algorithm Interpreter** that accepts user commands related to sorting integer arrays using different classic algorithms. The interpreter demonstrates key computing concepts: lexical analysis, command parsing, and procedural execution within a unified, interactive web interface.
    """)
    st.markdown("""
    The main objective is to let users experiment with and visualize various sorting algorithms side-by-side, deepening their understanding of each method's logic, performance, and process.
    """)
    st.markdown("### Sorting Algorithms Used")
    st.subheader("Bubble Sort")
    st.markdown("""
    - **Bubble Sort** repeatedly steps through the list, compares adjacent items, and swaps them if they are out of order.
    - It continues passing through the list until no swaps are needed, so the array is sorted.
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/0f/Insertion-sort-example-300px.gif", caption="Bubble Sort Example", use_container_width=True)
    st.subheader("Insertion Sort")
    st.markdown("""
    - **Insertion Sort** builds the sorted array one item at a time by comparing each new element to those already sorted, inserting it in the correct position.
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/7e/Insertion-sort-example.gif", caption="Insertion Sort Example", use_container_width=True)
    st.subheader("Quick Sort")
    st.markdown(""" 
    - **Quick Sort** selects a pivot and partitions the array into two sub-arrays: values less than the pivot and values greater, then recursively sorts the sub-arrays.
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6a/Sorting_quicksort_anim.gif", caption="Quick Sort Example", use_container_width=True)
    st.subheader("Merge Sort")
    st.markdown("""
    - **Merge Sort** is a divide-and-conquer algorithm: it splits the list into halves, recursively sorts each, and merges them together in order.
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/c/cc/Merge-sort-example-300px.gif", caption="Merge Sort Example", use_container_width=True)

elif st.session_state.page == "Details":
    st.title("Project Details")
    
    # Section I
    st.header("Section I. Introduction")
    st.write("""
    This project implements a Sorting Algorithm Interpreter, which reads user commands related to sorting arrays using different algorithms and executes them immediately. The interpreter demonstrates key programming language principles such as lexical analysis, parsing, and execution.
    """)
    st.image("https://miro.medium.com/v2/resize:fit:1400/1*yqRsMNxVL4OlhH4vNaKlSw.png", 
             caption="Programming Language Interpreter Flow", use_container_width=True)
    
    # Section II
    st.header("Section II. Description of the Input Language")
    st.subheader("Tokens")
    st.markdown("""
    - **Keywords:** SORT, BY, ASC, DESC, PRINT
    - **Sorting Algorithms:** BUBBLE, INSERTION, QUICK, MERGE
    - **Symbols:** `[`, `]`, `,`
    - **Numbers:** Integers
    - White spaces are ignored; invalid characters cause errors.
    """)
    
   
    st.image("https://media.geeksforgeeks.org/wp-content/uploads/20230706112910/Tokens-in-C.png", 
                 caption="Lexical Tokens Example", use_container_width=True)
   
    st.subheader("Grammar")
    st.write("The interpreter processes commands with the following structure:")
    st.code("""
    SORT [array] ALGORITHM BY ORDER
    PRINT
        """)
    
    # Section III
    st.header("Section III. System Design")
    st.write("""
    The system design of the Sorting Algorithm Interpreter emphasizes modularity and clarity throughout its structure. The interpreter consists of four primary components: **Lexer**, **Parser**, **Executor**, and an **Integrative Interface**.
    """)
    st.image("https://ruslanspivak.com/lsbasi-part7/lsbasi_part7_img01.png", 
             caption="Interpreter Architecture: Lexer → Parser → Executor", use_container_width=True)
    
    st.write("""
    When a user inputs a command, the **Lexer** first processes this command by breaking it down into interpretable tokens, systematically identifying keywords, numbers, and symbols.
    
    These tokens are then passed to the **Parser**, which analyzes the syntax and ensures the command adheres to language rules, constructing a structured command representation. Next, the **Executor** receives parsed commands and applies the specified sorting algorithm, organizing the inputted array in either ascending or descending order.
    
    The **Executor** also manages commands to print the most recently sorted array and supports several sorting methods including Bubble, Insertion, Quick, and Merge sorts. Error handling is distributed across each component, allowing the system to catch and describe errors in lexing, parsing, or execution with clear feedback to the user.
    """)
    
    # Section IV
    st.header("Section IV. Data Preprocessing and Cleaning")
    st.write("""
    The Data Preprocessing and Cleaning for this Sorting Algorithm Interpreter occurs primarily within the **Lexer (Lexical Analyzer)** component. When the user inputs a command, the Lexer scans the text, ignores irrelevant whitespace, and detects invalid characters early in the process.
    """)
    st.image("https://media.geeksforgeeks.org/wp-content/uploads/20230706113027/Lexical-Analysis.png", 
             caption="Lexical Analysis Process", use_container_width=True)
    
    # Section V
    st.header("Section V. Implementation Details")
    st.write("The implementation consists of three main components:")
    
    st.subheader("Lexer and Tokenizer")
    st.image("https://miro.medium.com/v2/resize:fit:1400/1*4rJVdq8IrZxGFd-2V6uFow.png", 
             caption="Tokenization Process", use_container_width=True)
    st.code("""
import re

class LexerError(Exception):
    pass

class Token:
    def __init__(self, type, value, position):
        self.type = type
        self.value = value
        self.position = position

class Lexer:
    token_specification = [
        ('SORT', r'SORT'),
        ('BY', r'BY'),
        ('ASC', r'ASC'),
        ('DESC', r'DESC'),
        ('PRINT', r'PRINT'),
        ('BUBBLE', r'BUBBLE'),
        ('INSERTION', r'INSERTION'),
        ('QUICK', r'QUICK'),
        ('MERGE', r'MERGE'),
        ('NUMBER', r'\\d+'),
        ('LBRACKET', r'\\['),
        ('RBRACKET', r'\\]'),
        ('COMMA', r','),
        ('MINUS', r'-'),
        ('SKIP', r'[ \\t]+'),
        ('MISMATCH', r'.'),
    ]
    """, language="python")
    
    st.subheader("Parser")
    st.write("The Parser analyzes tokens and builds command structures:")
    st.image("https://miro.medium.com/v2/resize:fit:1400/1*g2Y8rUGK1g0Tj5vHBvFJxw.png", 
             caption="Parsing Process", use_container_width=True)
    st.code("""
class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if tokens else None

    def parse(self):
        if self.current_token.type == 'SORT':
            return self.parse_sort_command()
        elif self.current_token.type == 'PRINT':
            return {'command': 'PRINT'}
    """, language="python")
    
    st.subheader("Executor")
    st.write("The Executor runs the sorting algorithms:")
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/c/c8/Bubble-sort-example-300px.gif", 
                 caption="Bubble Sort", use_container_width=True)
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/0/0f/Insertion-sort-example-300px.gif", 
                 caption="Insertion Sort", use_container_width=True)
    
    st.code("""
class Executor:
    def __init__(self):
        self.last_sorted_array = []

    def execute(self, command):
        if command['command'] == 'SORT':
            sorted_array = self.sort_array(
                command['array'], 
                command['algorithm'], 
                command['order']
            )
            self.last_sorted_array = sorted_array
    """, language="python")
    
    col3, col4 = st.columns(2)
    with col3:
        st.image("https://upload.wikimedia.org/wikipedia/commons/6/6a/Sorting_quicksort_anim.gif", 
                 caption="Quick Sort", use_container_width=True)
    with col4:
        st.image("https://upload.wikimedia.org/wikipedia/commons/c/cc/Merge-sort-example-300px.gif", 
                 caption="Merge Sort", use_container_width=True)
    
    # Section VI
    st.header("Section VI. Testing with Valid and Invalid Inputs")
    st.subheader("Valid Inputs")
    st.image("https://www.freecodecamp.org/news/content/images/2021/06/w-q-5.png", 
             caption="Valid Command Examples", use_container_width=True)
    st.code("""
SORT [5, 3, 8, 1, 13, 7, -9, -31] BUBBLE BY ASC
SORT [17, 10, 3, 9, -8, -2, -6] QUICK BY DESC
PRINT
SORT [2, -4, 1, -12, 3, 8, -9, 12] INSERTION BY ASC
SORT [4, -3, 5, 6, -9, 2, 7, 10, -15] MERGE BY DESC
    """)
    
    st.subheader("Invalid Inputs")
    st.image("https://miro.medium.com/v2/resize:fit:1400/1*xqFqTkqxG7aJvmZf6cFhVQ.png", 
             caption="Error Handling in Interpreters", use_container_width=True)
    st.code("""
SORT [5, 3, 8, 1, 13, 7, -9, -31,] BUBBLE BY ASC  # Trailing comma
SORT [5, 3, 8, 1, 13. 7, -9, -31] BUBBLE BY DESC  # Invalid character
SORT [17, 10, 3, 9, -8, -2, -6] BY DESC          # Missing algorithm
[2, -4, 1, -12, 3, 8, -9, 12] INSERTION BY ASC   # Missing SORT keyword
    """)
    
    # Section VII
    st.header("Section VII. Extensions and Additional Features")
    st.write("""
    In order to better display how our project works, we implemented a UI through the use of **Streamlit** to enable user-input and interactive visualization. 
    """)
    st.image("https://docs.streamlit.io/images/streamlit-community-cloud/deploy-an-app.png", 
             caption="Streamlit Interactive Dashboard", use_container_width=True)
    
    st.write("""
    The Streamlit interface provides:
    - Interactive input fields for array data
    - Algorithm selection dropdown
    - Order selection (Ascending/Descending)
    - Real-time visualization of sorting steps
    - Color-coded legend for value tracking
    """)
    
    # Section VIII
    st.header("Section VIII. Insights and Conclusions")
    st.write("""
    This Sorting Algorithm Interpreter project successfully demonstrates the fundamental principles of programming language design and implementation. Through the development of lexer, parser, and executor components, we gained hands-on experience with:
    """)
    st.image("https://miro.medium.com/v2/resize:fit:1400/1*cG6U1qstYDijh9bPL42e-Q.png", 
             caption="Compiler/Interpreter Design Principles", use_container_width=True)
    
    st.markdown("""
    - **Lexical Analysis:** Breaking down user input into tokens
    - **Syntax Parsing:** Validating command structure
    - **Algorithm Execution:** Implementing and comparing sorting algorithms
    - **Error Handling:** Providing clear feedback for invalid inputs
    - **Visualization:** Creating intuitive representations of algorithm behavior
    
    The modular design allows for easy extension with new algorithms and features, while the Streamlit interface makes the interpreter accessible and educational for users learning about sorting algorithms.
    """)
    
    # Section IX
    st.header("Section IX. References")
    st.image("https://images-na.ssl-images-amazon.com/images/I/51aflXy4WQL._SX379_BO1,204,203,200_.jpg", 
             caption="Compilers: Principles, Techniques, and Tools", width=300)
    st.markdown("""
    - Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Addison-Wesley.
    - Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
    - Python Software Foundation. (2024). *Python Documentation*. https://docs.python.org/
    - Streamlit Inc. (2024). *Streamlit Documentation*. https://docs.streamlit.io/
    """)

elif st.session_state.page == "Visualization":
    st.title("Sorting Algorithm Interpreter — Enhanced Visualizations")
    st.write("""
    You can enter a list of numbers (e.g., 5,3,8,1,7,4,3,3), choose the algorithm, and the order. Press 'Sort & Visualize' to see the sorting steps.
    """)
    st.caption("Supports Bubble, Insertion, Quick, and Merge Sort Algorithm.")

    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        input_list_str = st.text_input("Input List", value="")
    with c2:
        algorithm = st.selectbox("Algorithm", options=["Bubble", "Insertion", "Quick", "Merge"], index=0)
    with c3:
        order_choice = st.radio("Order", options=["ASC", "DESC"], index=0, horizontal=True)

    arr = []
    try:
        arr = [int(x) if x.strip().lstrip('-').isdigit() else None for x in input_list_str.strip().split(',')]
        arr = [x for x in arr if x is not None]
    except Exception:
        st.error("Invalid input: Please enter a comma-separated list of integers.")

    if st.button("Sort & Visualize"):
        if not arr:
            st.error("Input list is empty or invalid.")
        else:
            with st.spinner('Sorting...'):
                color_dict = get_color_dict(arr)
                if algorithm == 'Bubble':
                    history = bubble_sort_history(arr, order_choice)
                elif algorithm == 'Insertion':
                    history = insertion_sort_history(arr, order_choice)
                elif algorithm == 'Quick':
                    history = quick_sort_history(arr, order_choice)
                elif algorithm == 'Merge':
                    history = merge_sort_history(arr, order_choice)
                else:
                    st.warning("Algorithm not implemented.")
                    history = [arr[:]]

                st.subheader("Legend: Value-Color Mapping")
                fig_legend = plot_legend_bar(arr, color_dict)
                st.pyplot(fig_legend)

                st.subheader("Step-by-Step Sorting Visualization")
                fig_grid = plot_history_grid(history, color_dict, order_choice)
                st.pyplot(fig_grid)