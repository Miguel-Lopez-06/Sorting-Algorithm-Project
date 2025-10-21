import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")

# --- Sidebar Layout (pure Streamlit, left-aligned) ---
with st.sidebar:
    st.markdown("## Sorting Algorithm Interpreter Project")
    st.write("Pages")
    # Navigation state with pure Streamlit
    if "page" not in st.session_state:
        st.session_state.page = "Home Page"
    if st.button("  Home Page  "):
        st.session_state.page = "Home Page"
    if st.button("Sorting Algorithm Interpreter"):
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
    st.write("Contributor 1")
    st.write("Contributor 2")
    st.write("Contributor 3")

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
    st.image("https://upload.wikimedia.org/wikipedia/commons/c/c8/Bubble-sort-example-300px.gif", caption="Bubble Sort Example", use_column_width=True)
    st.subheader("Insertion Sort")
    st.markdown("""
    - **Insertion Sort** builds the sorted array one item at a time by comparing each new element to those already sorted, inserting it in the correct position.
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/7e/Insertion-sort-example.gif", caption="Insertion Sort Example", use_column_width=True)
    st.subheader("Quick Sort")
    st.markdown("""
    - **Quick Sort** selects a pivot and partitions the array into two sub-arrays: values less than the pivot and values greater, then recursively sorts the sub-arrays.
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6a/Sorting_quicksort_anim.gif", caption="Quick Sort Example", use_column_width=True)
    st.subheader("Merge Sort")
    st.markdown("""
    - **Merge Sort** is a divide-and-conquer algorithm: it splits the list into halves, recursively sorts each, and merges them together in order.
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/c/cc/Merge-sort-example-300px.gif", caption="Merge Sort Example", use_column_width=True)

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