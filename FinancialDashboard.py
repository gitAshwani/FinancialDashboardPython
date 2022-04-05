# -*- coding: utf-8 -*-
###############################################################################
# FINANCIAL DASHBOARD 2 - v1
###############################################################################

#==============================================================================
# Initiating
#==============================================================================
#importing all the required libraries
import pandas as pd
import matplotlib.pyplot as plt
import yahoo_fin.stock_info as si
import streamlit as st
import pandas_datareader.data as web
from datetime import datetime as dt
from datetime import timedelta
import numpy as np
from datetime import date
import mplfinance as mpf
import yfinance as yf
from plotly.subplots import make_subplots
import plotly.graph_objects as go


#==============================================================================
# Tab 1 Summary
#==============================================================================
#function to call if summary tab is clicked
def tab1():
    
    # Add dashboard title and description
    st.title(ticker)
    st.write("Data source: Yahoo Finance")
    st.header('Summary')
    if ticker != '-':
        #create columns to set the buttons used to customize the summary chart
        col21,col22,col23,col24,col25,col26,col27,col28,col29,col30,col31,col32 = st.columns(12)
        with col27: FinOpt1 = st.button('1M')
        with col28: FinOpt2 = st.button('3M')
        with col29: FinOpt3 = st.button('6M')
        with col30: FinOpt4 = st.button('YTD')
        with col31: FinOpt5 = st.button('1Y')
        with col32: FinOpt6 = st.button('3Y')
        col33,col34,col35,col36,col37,col38,col39,col40,col41,col42,col43,col44 = st.columns(12)
        with col39: FinOpt7 = st.button('5Y')
        with col40: FinOpt8 = st.button('MAX')
        #function to retrieve and return stock data
        @st.cache
        def GetSummary(ticker):
            return si.get_quote_table(ticker)
        
        #creating columns for table and chart separately
        col1,col2 = st.columns(2)
        info = GetSummary(ticker)
        summ = pd.DataFrame.from_dict(info, orient="index")
        summ[0] = summ[0].astype(str)
        col1.dataframe(summ, height=1000)
        #default data is of 3 years
        data=yf.download(tickers = ticker,period = "3y")
        #getting different data to present on chart as per intervals
        if FinOpt1:
            data=yf.download(tickers = ticker,period = "1mo")
        if FinOpt2:
            data=yf.download(tickers = ticker,period = "3mo")
        if FinOpt3:
            data=yf.download(tickers = ticker,period = "6mo")
        if FinOpt4:
            data=yf.download(tickers = ticker,period = "ytd")
        if FinOpt5:
            data=yf.download(tickers = ticker,period = "1y")
        if FinOpt6:
            data=yf.download(tickers = ticker,period = "3y")
        if FinOpt7:
            data=yf.download(tickers = ticker,period = "5y")
        if FinOpt8:
            data=yf.download(tickers = ticker)

        #plotting the chart using plotly library and subplots
        #adding bar chart for volumes and area for the closing price
        fig1 = make_subplots(specs=[[{"secondary_y": True}]])
        fig1.add_trace(go.Scatter(x=data.index,y=data['Close'],name='Close Price', fill='tozeroy'),secondary_y=False)
        fig1.add_trace(go.Bar(x=data.index,y=data['Volume'],name='Volume'),secondary_y=True)
        fig1.update_yaxes(range=[0,3000000000],secondary_y=True)
        fig1.update_yaxes(visible=False, secondary_y=True)
        col2.plotly_chart(fig1)

#==============================================================================
# Tab 2 Chart
#==============================================================================

def tab2():
    
    # Add dashboard title and description
    st.write("Data source: Yahoo Finance")
    st.header('Chart')
    
    # function to get data to plot charts
    @st.cache
    def GetData(ticker):
        return si.get_data(ticker)

    if ticker != '-':
        #creating start date and end date buttons to select date range to plot charts
        col221, col222 = st.columns(2)
        start_date1 = col221.date_input("Start date", dt.today().date() - timedelta(days=366))
        end_date1 = col222.date_input("End date", dt.today().date()  - timedelta(days=1))
        
        #creating drop down to select interval to show data
        interval1 = st.selectbox("Select an interval:", ['Day','Week','Month'])
        if interval1 == 'Month':
            interval = '1mo'
        elif interval1 == 'Week':
            interval = '1wk'
        else:
            interval = '1d'
            
        st.write("Select date range or duration:")
        #creating columns to create buttons to select the duration of data
        col21,col22,col23,col24,col25,col26,col27,col28= st.columns(8)
        with col21: FinOpt1 = st.button('1M')
        with col22: FinOpt2 = st.button('3M')
        with col23: FinOpt3 = st.button('6M')
        with col24: FinOpt4 = st.button('YTD')
        with col25: FinOpt5 = st.button('1Y')
        with col26: FinOpt6 = st.button('3Y')
        with col27: FinOpt7 = st.button('5Y')
        with col28: FinOpt8 = st.button('MAX')
        
        #getting data based on the selected duration
        data=yf.download(tickers = ticker, period='1y', interval='1d')
        if FinOpt1:
            data=yf.download(tickers = ticker,period = "1mo", interval=interval)
        elif FinOpt2:
            data=yf.download(tickers = ticker,period = "3mo", interval=interval)
        elif FinOpt3:
            data=yf.download(tickers = ticker,period = "6mo", interval=interval)
        elif FinOpt4:
            data=yf.download(tickers = ticker,period = "ytd", interval=interval)
        elif FinOpt5:
            data=yf.download(tickers = ticker,period = "1y", interval=interval)
        elif FinOpt6:
            data=yf.download(tickers = ticker,period = "3y", interval=interval)
        elif FinOpt7:
            data=yf.download(tickers = ticker,period = "5y", interval=interval)
        elif FinOpt8:
            data=yf.download(tickers = ticker)
        else:
            data = web.get_data_yahoo(ticker, start_date1, end_date1)
        #dropping the na values from the data
        data2 = data.dropna()
        
        #plotting 4 types of chart using plotly and mplfinance
        chart_type = st.radio("Choose Chart Type", ['Line (mplfinance)','Line (plotly)','Candle (mplfinance)','Candle (plotly)'])
        if chart_type == 'Line (mplfinance)':
            a = mpf.plot(data2,type='line',mav=50,volume=True, tight_layout = True)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot(a)
        elif chart_type == 'Line (plotly)':
            fig1 = make_subplots(specs=[[{"secondary_y": True}]])
            fig1.add_trace(go.Scatter(x=data2.index,y=data2['Close'],name='Close Price'),secondary_y=False)
            fig1.add_trace(go.Scatter(x=data2.index,y=data2['Close'].rolling(window=50).mean(),marker_color='red',name='50 Day MA'))
            fig1.add_trace(go.Bar(x=data2.index,y=data2['Volume'],name='Volume'),secondary_y=True)
            fig1.update_yaxes(range=[0,3000000000],secondary_y=True)
            fig1.update_yaxes(visible=False, secondary_y=True)
            st.plotly_chart(fig1)
        elif chart_type == 'Candle (mplfinance)':
            a = mpf.plot(data2,type='candle',mav=50,volume=True, tight_layout = True)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot(a)
        elif chart_type == 'Candle (plotly)':
            fig1 = make_subplots(specs=[[{"secondary_y": True}]])
            fig1.add_trace(go.Candlestick(x=data2.index,
                                              open=data2['Open'],
                                              high=data2['High'],
                                              low=data2['Low'],
                                              close=data2['Close'],
                                              name='Stock'))
            fig1.add_trace(go.Scatter(x=data2.index,y=data2['Close'].rolling(window=50).mean(),marker_color='blue',name='50 Day MA'))
            fig1.add_trace(go.Bar(x=data2.index, y=data2['Volume'], name='Volume'),secondary_y=True)
            #fig3.update_layout(title={'text':'TSLA', 'x':0.5})
            fig1.update_yaxes(range=[0,1000000000],secondary_y=True)
            fig1.update_yaxes(visible=False, secondary_y=True)
            st.plotly_chart(fig1)
        

#==============================================================================
# Tab 3 Statistics
#==============================================================================   
def tab3():
    
    # Add dashboard title and description
    st.title(ticker)
    st.write("Data source: Yahoo Finance")
    st.header('Statistics')
    
    # Add table to show stock data
    @st.cache
    def GetStats(tickers, start_date, end_date):
        return si.get_stats(ticker)   
    
    if ticker != '-':
        #to get data and show in streamlit
        stats = GetStats(ticker, start_date, end_date)
        st.dataframe(stats, height=1500)
#==============================================================================
# Tab 4 Financials
#==============================================================================
def tab4():
    # Add dashboard title and description
    st.title(ticker)
    st.write("Data source: Yahoo Finance")
    st.header('Financial')
    
    if ticker != '-':
        #to choose between the intervals and type of data
        view = st.selectbox("Choose intervals:", ['Yearly','Quarterly'])    
        col1, col2, col3, col4 = st.columns(4)
        with col1: FinOpt1 = st.button('Income Statement')
        with col2: FinOpt2 = st.button('Balance Sheet')
        with col3: FinOpt3 = st.button('Cash Flow')
       
        #to get and show the dataframe as per the above selection
        info = si.get_income_statement(ticker)
        if FinOpt1 and view == 'Quarterly':
            info = si.get_income_statement(ticker, yearly=False)
        elif FinOpt1 and view == 'Yearly':
            info = si.get_income_statement(ticker, yearly=True)
        elif FinOpt2 and view == 'Quarterly':
            info = si.get_balance_sheet(ticker, yearly=False)
        elif FinOpt2 and view == 'Yearly':
            info = si.get_balance_sheet(ticker, yearly=True)
        elif FinOpt3 and view == 'Quarterly':
            info = si.get_cash_flow(ticker, yearly=False)
        elif FinOpt3 and view == 'Yearly':
            info = si.get_cash_flow(ticker, yearly=True)

        st.dataframe(info, height=1000)

#==============================================================================
# Tab 5 Analysis
#==============================================================================
def tab5():
    # Add dashboard title and description
    st.title(ticker)
    st.write("Data source: Yahoo Finance")
    st.header('Analysis')
    
    @st.cache
    def GetDetails(ticker):
            return si.get_analysts_info(ticker)
    
    if ticker != '-':
        #to get data and show it in streamlit
        info = GetDetails(ticker)
        for key,values in info.items():        
            sum1 = pd.DataFrame(info[key])
            st.dataframe(sum1, height=1000, width=1000)
    
#==============================================================================
# Tab 6 Monte-Carlo Simulation
#==============================================================================
def tab6():
    # Add dashboard title and description
    st.title(ticker)
    st.write("Data source: Yahoo Finance")
    st.header('Monte Carlo Simulation')
    
    @st.cache
    def GetData(ticker):
        return si.get_data(ticker)
    
    if ticker != '-':
        #to get data to manipulate and do simulations
        info = GetData(ticker)
        close_price = info['close']
        # The returns ((today price - yesterday price) / yesterday price)
        daily_return = close_price.pct_change()
        # The volatility (high value, high risk)
        daily_volatility = np.std(daily_return)
        # Setup the Monte Carlo simulation
        np.random.seed(123)
        #to select the number of simulations and time horizons
        simulations = st.selectbox("Select number of Simulations:", [200,500,1000])
        time_horizone = st.selectbox("Select time horizon:", [30,60,90])
        
        # Run the simulation
        simulation_df = pd.DataFrame()
        
        for i in range(simulations):
            
            # The list to store the next stock price
            next_price = []
            
            # Create the next stock price
            last_price = close_price[-1]
            
            for j in range(time_horizone):
                # Generate the random percentage change around the mean (0) and std (daily_volatility)
                future_return = np.random.normal(0, daily_volatility)
        
                # Generate the random future price
                future_price = last_price * (1 + future_return)
        
                # Save the price and go next
                next_price.append(future_price)
                last_price = future_price
            
            # Store the result of the simulation
            simulation_df[i] = next_price
        
        # Plot the simulation stock price in the future
        fig, ax = plt.subplots()
        fig.set_size_inches(15, 10, forward=True)
        
        plt.plot(simulation_df)
        plt.title('Monte Carlo simulation for AAPL stock price in next 200 days')
        plt.xlabel('Day')
        plt.ylabel('Price')
        
        plt.axhline(y=close_price[-1], color='red')
        plt.legend(['Current stock price is: ' + str(np.round(close_price[-1], 2))])
        ax.get_legend().legendHandles[0].set_color('red')
        
        st.pyplot(plt)
        
        ending_price = simulation_df.iloc[-1:, :].values[0, ]
        # Price at 95% confidence interval
        future_price_95ci = np.percentile(ending_price, 5)
        
        # Value at Risk
        VaR = close_price[-1] - future_price_95ci
        st.subheader('VaR at 95% confidence interval is: ' + str(np.round(VaR, 2)) + ' USD')
#==============================================================================
# Tab 7 Company Profile
#==============================================================================
def tab7():
    
    # Add dashboard title and description
    st.title(ticker)
    st.write("Data source: Yahoo Finance")
    st.header('Company profile')
    
    # Add table to show stock data
    @st.cache
    def GetCompanyInfo(ticker):
        return si.get_company_info(ticker)
    
    if ticker != '-':
        info = GetCompanyInfo(ticker)
        info['Value'] = info['Value'].astype(str)
        st.dataframe(info, height=1000)

#==============================================================================
# Main body
#==============================================================================

def run():
    
    # Add the ticker selection on the sidebar
    # Get the list of stock tickers from S&P500
    ticker_list = ['-'] + si.tickers_sp500()
    
    # Add selection box
    global ticker
    ticker = st.sidebar.selectbox("Select a ticker", ticker_list)
    st.title("Financial Dashboard")
    

    # Add select begin-end date
    global start_date, end_date
    col1, col2 = st.sidebar.columns(2)
    start_date = col1.date_input("Start date", dt.today().date() - timedelta(days=30))
    end_date = col2.date_input("End date", dt.today().date())
    
    #to update the data and refresh
    with st.sidebar.form(key = "Refresh Form"):
        st.form_submit_button(label = "Update")
    
    # Add a radio box
    select_tab = st.sidebar.radio("Select tab", ['Summary', 'Chart','Statistics','Financial','Analysis',
                                                 'Monte Carlo Simulation', 'Company Profile'])
    
    # Show the selected tab
    if select_tab == 'Summary':
        # Run tab 1
        tab1()
    elif select_tab == 'Chart':
        # Run tab 2
        tab2()
    elif select_tab == 'Statistics':
        # Run tab 3
        tab3()
    elif select_tab == 'Financial':
        # Run tab 4
        tab4()
    elif select_tab == 'Analysis':
        # Run tab 5
        tab5()
    elif select_tab == 'Monte Carlo Simulation':
        # Run tab 6
        tab6()
    elif select_tab == 'Company Profile':
        # Run tab 7
        tab7()
        
if __name__ == "__main__":
    run()
    
###############################################################################
# END
###############################################################################