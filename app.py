import requests
import streamlit as st

def retrieve_sol_price():
    url = 'https://min-api.cryptocompare.com/data/price?fsym=SOL&tsyms=USDC'
    response = requests.get(url)
    if not response.ok:
        st.exception(response)
    data = response.json()
    return data['USDC']

def borrow_capacity( collateral_amount, collateral_ltv_pct, borrow_factor ):
  collateral_ltv = collateral_ltv_pct / 100
  return ( collateral_amount * collateral_ltv ) / borrow_factor

def price_at_ltv( dept, collateral, borrowing_factor, ltv_pct ):
  return ltv_pct * collateral / ( dept * borrowing_factor * 100 )

usdc_column, sol_column = st.columns(2)
with usdc_column.expander('USDC parameters'):
    st.text_input('Max LTV %', value=79.2, key='usdc_max_ltv_pct')
    st.text_input('Liquidation LTV %', value=90, key='usdc_liquidation_ltv_pct')
    st.text_input('Borrow factor', value=1, key='usdc_borrow_factor')
with sol_column.expander('SOL parameters'):
    st.text_input('Max LTV %', value=65, key='solana_max_ltv_pct')
    st.text_input('Liquidation LTV %', value=75, key='solana_liquidation_ltv_pct')
    st.text_input('Borrow factor', value=1.25, key='solana_borrow_factor')

st.text_input('Collateral USDC', value=1000, key='usdc_collateral_amount')

solana_price_usdc = retrieve_sol_price()
st.markdown(f"##### :blue[1 SOL = {solana_price_usdc} USDC]")

borrow_capacity_usdc = borrow_capacity( float(st.session_state.usdc_collateral_amount), float(st.session_state.usdc_max_ltv_pct), float(st.session_state.solana_borrow_factor) )
borrow_capacity_sol = borrow_capacity_usdc / solana_price_usdc

c = st.container()
col1, col2 = c.columns(2)
col1.markdown("##### Capacity USDC")
col2.markdown(f"##### :blue[{round(borrow_capacity_usdc, 2)}]")
col1, col2 = c.columns(2)
col1.markdown("##### Capacity SOL")
col2.markdown(f"##### :blue[{round(borrow_capacity_sol, 6)}]")


curernt_solana_price = solana_price_usdc
current_ltv = ((borrow_capacity_sol * curernt_solana_price * float(st.session_state.solana_borrow_factor)) / float(st.session_state.usdc_collateral_amount)) * 100
sol_price_at_max_pool_ltv = price_at_ltv( borrow_capacity_sol, float(st.session_state.usdc_collateral_amount), float(st.session_state.solana_borrow_factor), float(st.session_state.usdc_max_ltv_pct) )
sol_price_at_85_ltv = price_at_ltv( borrow_capacity_sol, float(st.session_state.usdc_collateral_amount), float(st.session_state.solana_borrow_factor), 85 )
sol_price_at_90_ltv = price_at_ltv( borrow_capacity_sol, float(st.session_state.usdc_collateral_amount), float(st.session_state.solana_borrow_factor), 90 )
sol_ltv85_pct_change = ( sol_price_at_85_ltv / sol_price_at_max_pool_ltv - 1 ) * 100
sol_ltv90_pct_change = ( sol_price_at_90_ltv / sol_price_at_max_pool_ltv - 1 ) * 100

c = st.container()
col1, col2 = c.columns(2)
col1.markdown(f"##### LTV {float(st.session_state.usdc_max_ltv_pct)}")
col2.markdown(f"##### :green[{round(sol_price_at_max_pool_ltv, 2)}]")
col1, col2 = c.columns(2)
col1.markdown(f"##### LTV 85")
col2.markdown(f"##### :orange[{round(sol_price_at_85_ltv, 2)} ~ {round(sol_ltv85_pct_change, 2)}%]")
col1, col2 = c.columns(2)
col1.markdown(f"##### LTV 90")
col2.markdown(f"##### :red[{round(sol_price_at_90_ltv, 2)} ~ {round(sol_ltv90_pct_change, 2)}%]")