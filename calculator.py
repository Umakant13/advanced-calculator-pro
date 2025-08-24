import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from forex_python.converter import CurrencyRates
from pint import UnitRegistry
import math
import operator
import requests  # <-- Add this line

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Advanced Calculator Pro", layout="wide")
st.title("🧮 Advanced Calculator Pro")

# --- MODE SELECTION IN SIDEBAR ---
# Using a key ensures the selectbox itself doesn't cause rerendering issues
mode = st.sidebar.selectbox("Select Mode:", [
    "Calculator", "Programmer", "Converters", "Data Analysis", "Graphing"
], key="mode_select")

# --- STATE INITIALIZATION ---
def initialize_state(prefix, default_value='0'):
    """Initializes session state variables for a given mode to prevent conflicts."""
    if f'display_{prefix}' not in st.session_state:
        st.session_state[f'display_{prefix}'] = default_value
    if f'first_operand_{prefix}' not in st.session_state:
        st.session_state[f'first_operand_{prefix}'] = None
    if f'operator_{prefix}' not in st.session_state:
        st.session_state[f'operator_{prefix}'] = None
    if f'new_input_{prefix}' not in st.session_state:
        st.session_state[f'new_input_{prefix}'] = True
    if prefix == 'data' and 'data_list' not in st.session_state:
        st.session_state.data_list = []

# =====================================================================
# ========= EACH MODE IS IN ITS OWN CONTAINER TO PREVENT UI BUGS ======
# =====================================================================

# ------------------------- CALCULATOR MODE ---------------------------
if mode == "Calculator":
    with st.container():
        st.subheader("Scientific Calculator")
        initialize_state('calc')

        # --- Handler Functions ---
        def handle_calc_number(num_str):
            if num_str in ['π', 'e']:
                val = str(math.pi if num_str == 'π' else math.e)
                st.session_state.display_calc = val; st.session_state.new_input_calc = False
                return
            if st.session_state.new_input_calc:
                st.session_state.display_calc = num_str; st.session_state.new_input_calc = False
            elif st.session_state.display_calc == '0' and num_str != '.':
                st.session_state.display_calc = num_str
            elif not (num_str == '.' and '.' in st.session_state.display_calc):
                st.session_state.display_calc += num_str

        def perform_calculation():
            try:
                op = st.session_state.operator_calc; first = float(st.session_state.first_operand_calc); second = float(st.session_state.display_calc)
                ops = {'+': operator.add, '−': operator.sub, '×': operator.mul, '÷': operator.truediv, 'xʸ': operator.pow}
                result = "Error" if op == '÷' and second == 0 else ops[op](first, second)
                if isinstance(result, float) and result.is_integer(): result = int(result)
                st.session_state.display_calc = str(result); st.session_state.first_operand_calc = result
            except: st.session_state.display_calc = "Error"
            st.session_state.new_input_calc = True

        def handle_calc_operator(op):
            if st.session_state.operator_calc and not st.session_state.new_input_calc: perform_calculation()
            st.session_state.first_operand_calc = float(st.session_state.display_calc); st.session_state.operator_calc = op; st.session_state.new_input_calc = True

        def handle_equals():
            if st.session_state.operator_calc and st.session_state.first_operand_calc is not None: perform_calculation()
            st.session_state.operator_calc = None

        def handle_unary_op(op):
            try:
                val = float(st.session_state.display_calc)
                ops = {'√': math.sqrt, 'x²': lambda x: x**2, 'ln': math.log, 'log': math.log10, '1/x': lambda x: 1/x, 'n!': lambda x: math.factorial(int(x)), 'sin': lambda x: math.sin(math.radians(x)), 'cos': lambda x: math.cos(math.radians(x)), 'tan': lambda x: math.tan(math.radians(x))}
                result = ops[op](val)
                if isinstance(result, float) and result.is_integer(): result = int(result)
                st.session_state.display_calc = str(result)
            except: st.session_state.display_calc = "Error"
            st.session_state.new_input_calc = True

        def handle_clear(): initialize_state('calc')
        def handle_backspace():
            if not st.session_state.new_input_calc and len(st.session_state.display_calc) > 1: st.session_state.display_calc = st.session_state.display_calc[:-1]
            else: st.session_state.display_calc = '0'; st.session_state.new_input_calc = True

        # --- UI Layout with unique keys for all buttons ---
        st.text_input("Display", st.session_state.display_calc, disabled=True, key="calc_display")
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.button('sin', key='calc_sin', on_click=handle_unary_op, args=('sin',), use_container_width=True)
        c1.button('√', key='calc_sqrt', on_click=handle_unary_op, args=('√',), use_container_width=True)
        c1.button('7', key='calc_7', on_click=handle_calc_number, args=('7',), use_container_width=True)
        c1.button('4', key='calc_4', on_click=handle_calc_number, args=('4',), use_container_width=True)
        c1.button('1', key='calc_1', on_click=handle_calc_number, args=('1',), use_container_width=True)
        c1.button('0', key='calc_0', on_click=handle_calc_number, args=('0',), use_container_width=True)

        c2.button('cos', key='calc_cos', on_click=handle_unary_op, args=('cos',), use_container_width=True)
        c2.button('x²', key='calc_sq', on_click=handle_unary_op, args=('x²',), use_container_width=True)
        c2.button('8', key='calc_8', on_click=handle_calc_number, args=('8',), use_container_width=True)
        c2.button('5', key='calc_5', on_click=handle_calc_number, args=('5',), use_container_width=True)
        c2.button('2', key='calc_2', on_click=handle_calc_number, args=('2',), use_container_width=True)
        c2.button('.', key='calc_.', on_click=handle_calc_number, args=('.',), use_container_width=True)
        
        c3.button('tan', key='calc_tan', on_click=handle_unary_op, args=('tan',), use_container_width=True)
        c3.button('xʸ', key='calc_pow', on_click=handle_calc_operator, args=('xʸ',), use_container_width=True)
        c3.button('9', key='calc_9', on_click=handle_calc_number, args=('9',), use_container_width=True)
        c3.button('6', key='calc_6', on_click=handle_calc_number, args=('6',), use_container_width=True)
        c3.button('3', key='calc_3', on_click=handle_calc_number, args=('3',), use_container_width=True)
        c3.button('=', key='calc_eq', on_click=handle_equals, use_container_width=True, type="primary")

        c4.button('log', key='calc_log', on_click=handle_unary_op, args=('log',), use_container_width=True)
        c4.button('1/x', key='calc_inv', on_click=handle_unary_op, args=('1/x',), use_container_width=True)
        c4.button('C', key='calc_C', on_click=handle_clear, use_container_width=True)
        c4.button('÷', key='calc_div', on_click=handle_calc_operator, args=('÷',), use_container_width=True)
        c4.button('×', key='calc_mul', on_click=handle_calc_operator, args=('×',), use_container_width=True)
        c4.button('−', key='calc_sub', on_click=handle_calc_operator, args=('−',), use_container_width=True)

        c5.button('ln', key='calc_ln', on_click=handle_unary_op, args=('ln',), use_container_width=True)
        c5.button('n!', key='calc_fact', on_click=handle_unary_op, args=('n!',), use_container_width=True)
        c5.button('←', key='calc_bsp', on_click=handle_backspace, use_container_width=True)
        c5.button('π', key='calc_pi', on_click=handle_calc_number, args=('π',), use_container_width=True)
        c5.button('e', key='calc_e', on_click=handle_calc_number, args=('e',), use_container_width=True)
        c5.button('+', key='calc_add', on_click=handle_calc_operator, args=('+',), use_container_width=True)

# ------------------------ PROGRAMMER MODE ----------------------------
elif mode == "Programmer":
    with st.container():
        st.subheader("Programmer & Bitwise Calculator")
        initialize_state('prog')

        def handle_prog_number(n):
            if st.session_state.new_input_prog or st.session_state.display_prog == '0':
                st.session_state.display_prog = n
                st.session_state.new_input_prog = False
            else:
                st.session_state.display_prog += n
        
        def handle_prog_operator(op):
            st.session_state.first_operand_prog = int(st.session_state.display_prog)
            st.session_state.operator_prog = op
            st.session_state.new_input_prog = True

        def handle_prog_equals():
            if not st.session_state.operator_prog: return
            try:
                first = st.session_state.first_operand_prog
                second = int(st.session_state.display_prog)
                op = st.session_state.operator_prog
                ops = {'AND': operator.and_, 'OR': operator.or_, 'XOR': operator.xor}
                st.session_state.display_prog = str(ops[op](first, second))
            except:
                st.session_state.display_prog = "Error"
            st.session_state.operator_prog = None
            st.session_state.new_input_prog = True
            
        def handle_prog_not():
            st.session_state.display_prog = str(~(int(st.session_state.display_prog)))
            st.session_state.new_input_prog = True

        display_col, keypad_col = st.columns([2, 1.5])
        with display_col:
            st.markdown("#### Conversions")
            num = int(st.session_state.display_prog) if st.session_state.display_prog.lstrip('-').isdigit() else 0
            st.text_input("Decimal", value=num, disabled=True, key='prog_dec')
            st.text_input("Hexadecimal", value=hex(num).upper(), disabled=True, key='prog_hex')
            st.text_input("Binary", value=bin(num), disabled=True, key='prog_bin')
        
        with keypad_col:
            st.button("Clear", key='prog_C', on_click=lambda: initialize_state('prog'), use_container_width=True)
            c1, c2, c3 = st.columns(3)
            c1.button('7', key='prog_7', on_click=handle_prog_number, args=('7',), use_container_width=True)
            c2.button('8', key='prog_8', on_click=handle_prog_number, args=('8',), use_container_width=True)
            c3.button('9', key='prog_9', on_click=handle_prog_number, args=('9',), use_container_width=True)
            c1.button('4', key='prog_4', on_click=handle_prog_number, args=('4',), use_container_width=True)
            c2.button('5', key='prog_5', on_click=handle_prog_number, args=('5',), use_container_width=True)
            c3.button('6', key='prog_6', on_click=handle_prog_number, args=('6',), use_container_width=True)
            c1.button('1', key='prog_1', on_click=handle_prog_number, args=('1',), use_container_width=True)
            c2.button('2', key='prog_2', on_click=handle_prog_number, args=('2',), use_container_width=True)
            c3.button('3', key='prog_3', on_click=handle_prog_number, args=('3',), use_container_width=True)
            c2.button('0', key='prog_0', on_click=handle_prog_number, args=('0',), use_container_width=True)
            
            st.markdown("---")
            st.markdown("Bitwise Operations")
            b1, b2 = st.columns(2)
            b1.button("AND", key='prog_and', on_click=handle_prog_operator, args=("AND",), use_container_width=True)
            b2.button("OR", key='prog_or', on_click=handle_prog_operator, args=("OR",), use_container_width=True)
            b1.button("XOR", key='prog_xor', on_click=handle_prog_operator, args=("XOR",), use_container_width=True)
            b2.button("NOT", key='prog_not', on_click=handle_prog_not, use_container_width=True)
            st.button("=", key='prog_eq', on_click=handle_prog_equals, use_container_width=True, type="primary")

# -------------------------- CONVERTERS MODE --------------------------
elif mode == "Converters":
    with st.container():
        st.subheader("Unit Converters")
        initialize_state('conv')
        
        # --- Helper function for currency conversion ---
        @st.cache_data(ttl=3600) # Cache results for 1 hour to avoid excessive API calls
        def get_currency_data():
            try:
                response = requests.get("https://api.frankfurter.app/currencies")
                if response.status_code == 200:
                    return sorted(list(response.json().keys()))
            except:
                return ["INR", "USD", "EUR", "GBP", "JPY"] # Fallback list
        
        def handle_conv_number(n):
            if st.session_state.new_input_conv or st.session_state.display_conv == '0':
                st.session_state.display_conv = n; st.session_state.new_input_conv = False
            elif not (n == '.' and '.' in st.session_state.display_conv):
                st.session_state.display_conv += n
        
        # --- UI Layout ---
        keypad_col, conversion_col = st.columns([1, 2])
        with keypad_col:
            st.text_input("Value to Convert", st.session_state.display_conv, disabled=True, key='conv_display')
            st.button("Clear Value", key='conv_C', on_click=lambda: initialize_state('conv'), use_container_width=True)
            k1,k2,k3 = st.columns(3)
            k1.button('7', key='conv_7', on_click=handle_conv_number, args=('7',), use_container_width=True); k2.button('8', key='conv_8', on_click=handle_conv_number, args=('8',), use_container_width=True); k3.button('9', key='conv_9', on_click=handle_conv_number, args=('9',), use_container_width=True)
            k1.button('4', key='conv_4', on_click=handle_conv_number, args=('4',), use_container_width=True); k2.button('5', key='conv_5', on_click=handle_conv_number, args=('5',), use_container_width=True); k3.button('6', key='conv_6', on_click=handle_conv_number, args=('6',), use_container_width=True)
            k1.button('1', key='conv_1', on_click=handle_conv_number, args=('1',), use_container_width=True); k2.button('2', key='conv_2', on_click=handle_conv_number, args=('2',), use_container_width=True); k3.button('3', key='conv_3', on_click=handle_conv_number, args=('3',), use_container_width=True)
            k1.button('0', key='conv_0', on_click=handle_conv_number, args=('0',), use_container_width=True); k2.button('.', key='conv_.', on_click=handle_conv_number, args=('.',), use_container_width=True)

        with conversion_col:
            ureg = UnitRegistry(autoconvert_offset_to_baseunit=True)
            units = {"Length": ["meter", "kilometer", "mile", "foot", "inch"], "Mass": ["gram", "kilogram", "pound", "ounce"], "Temperature": ["celsius", "fahrenheit", "kelvin"], "Data Storage": ["byte", "kilobyte", "megabyte", "gigabyte"]}
            converter_type = st.selectbox("Select converter type:", ["Currency"] + list(units.keys()), key='conv_type')
            
            value_to_convert = float(st.session_state.display_conv) if st.session_state.display_conv else 0.0

            if converter_type != "Currency":
                c1, c2 = st.columns(2)
                from_unit = c1.selectbox("From unit:", units.get(converter_type, []), key='conv_from_unit')
                to_unit = c2.selectbox("To unit:", units.get(converter_type, []), key='conv_to_unit')
                result = (value_to_convert * ureg(from_unit)).to(to_unit)
                st.success(f"**Result:** {value_to_convert} {from_unit} = {result:~P.4f}")
            
            else: # Currency Conversion using API
                c1, c2 = st.columns(2)
                currencies = get_currency_data()
                from_curr = c1.selectbox("From:", currencies, index=currencies.index("USD") if "USD" in currencies else 0, key='conv_from_curr')
                to_curr = c2.selectbox("To:", currencies, index=currencies.index("EUR") if "EUR" in currencies else 1, key='conv_to_curr')

                if st.button("Convert Currency", key='conv_trigger', use_container_width=True, type='primary'):
                    try:
                        response = requests.get(f"https://api.frankfurter.app/latest?amount={value_to_convert}&from={from_curr}&to={to_curr}")
                        if response.status_code == 200:
                            data = response.json()
                            rate = data['rates'][to_curr]
                            st.success(f"**Result:** {value_to_convert} {from_curr} = {rate:.2f} {to_curr}")
                        else:
                            st.error(f"Error from API: {response.text}")
                    except Exception as e:
                        st.error(f"Could not connect to currency service. Error: {e}")

# -------------------------- DATA ANALYSIS MODE -----------------------
elif mode == "Data Analysis":
    with st.container():
        st.subheader("Statistical Analysis & Visualization")
        initialize_state('data')

        def add_from_keypad():
            try:
                st.session_state.data_list.append(float(st.session_state.display_data))
                st.session_state.display_data = '0' # Clear for next entry
            except:
                st.error("Invalid number in keypad")
        
        def load_from_textarea():
            try:
                if text_data := st.session_state.data_text_area.strip():
                    st.session_state.data_list = [float(x.strip()) for x in text_data.split(',')]
            except:
                st.error("Invalid format in text area. Use comma-separated numbers.")
        
        def handle_data_keypad(n):
            if st.session_state.display_data == '0':
                st.session_state.display_data = n
            else:
                st.session_state.display_data += n

        c1, c2 = st.columns([1.5, 2])
        with c1:
            st.markdown("#### Input Data")
            st.text_area("Paste comma-separated data:", key="data_text_area", on_change=load_from_textarea)
            st.text_input("Or enter number on keypad:", value=st.session_state.display_data, disabled=True, key='data_display')
            
            k1,k2,k3 = st.columns(3)
            k1.button('7', key='data_7', on_click=handle_data_keypad, args=('7',), use_container_width=True)
            k2.button('8', key='data_8', on_click=handle_data_keypad, args=('8',), use_container_width=True)
            k3.button('9', key='data_9', on_click=handle_data_keypad, args=('9',), use_container_width=True)
            k1.button('4', key='data_4', on_click=handle_data_keypad, args=('4',), use_container_width=True)
            k2.button('5', key='data_5', on_click=handle_data_keypad, args=('5',), use_container_width=True)
            k3.button('6', key='data_6', on_click=handle_data_keypad, args=('6',), use_container_width=True)
            k1.button('1', key='data_1', on_click=handle_data_keypad, args=('1',), use_container_width=True)
            k2.button('2', key='data_2', on_click=handle_data_keypad, args=('2',), use_container_width=True)
            k3.button('3', key='data_3', on_click=handle_data_keypad, args=('3',), use_container_width=True)
            k1.button('0', key='data_0', on_click=handle_data_keypad, args=('0',), use_container_width=True)
            k2.button('.', key='data_.', on_click=handle_data_keypad, args=('.',), use_container_width=True)
            
            st.button("Add Number to List", key='data_add', on_click=add_from_keypad, use_container_width=True, type="primary")
            st.button("Clear List", key='data_clear', on_click=lambda: st.session_state.update(data_list=[]), use_container_width=True)

        with c2:
            st.markdown(f"#### Analysis for {len(st.session_state.data_list)} Data Points")
            if st.session_state.data_list:
                data = np.array(st.session_state.data_list)
                st.write(f"**Data Set:** `{st.session_state.data_list}`")
                st.write(f"**Mean:** `{np.mean(data):.4f}` | **Median:** `{np.median(data):.4f}` | **Std Dev:** `{np.std(data):.4f}`")
                fig, ax = plt.subplots()
                ax.hist(data, bins='auto', edgecolor='black')
                ax.set_title("Histogram")
                st.pyplot(fig)
            else:
                st.info("Enter data to see analysis.")

# -------------------------- GRAPHING MODE ----------------------------
elif mode == "Graphing":
    with st.container():
        st.subheader("Multi-Function Graphing Calculator")
        st.info("Plot multiple functions by separating them with a semicolon ';'. Ex: `np.sin(x); np.cos(x)`")
        function_str = st.text_input("Functions f(x):", "x**2; -x**2", key='graph_input')
        
        if st.button("Plot Functions", key='graph_plot'):
            functions = [f.strip() for f in function_str.split(';') if f.strip()]
            x = np.linspace(-10, 10, 400)
            fig, ax = plt.subplots()
            try:
                for func in functions:
                    y = eval(func, {"np": np}, {"x": x})
                    ax.plot(x, y, label=func)
                ax.grid(True)
                ax.legend()
                ax.set_xlabel("x")
                ax.set_ylabel("f(x)")
                st.pyplot(fig)
            except Exception as e:
                st.error(f"Invalid function syntax: {e}")
