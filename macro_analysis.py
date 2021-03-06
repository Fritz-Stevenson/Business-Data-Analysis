import pandas as pd
import bokeh
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models import HoverTool
class dataframe_analysis:
    def __init__(self, csv):
        self.csv = csv

    def avg_discount_rate(self):
        pd.to_numeric(self.csv['Discount_Amount'])
        pd.to_numeric(self.csv['Order_Total_Amount'])
        total_sales_amount = self.csv['Order_Total_Amount'].sum()
        total_discount_amount = self.csv['Discount_Amount'].sum()
        total_discount_avg = int((total_discount_amount / (total_discount_amount+total_sales_amount))*100)
        return print(f'Customer Discount Avg: {total_discount_avg}%')


    def customer_role_breakdown(self):
        retail = 0
        wholesale = 0
        sum_count =int(len(self.csv.index))
        for i, row in self.csv.iterrows():
            if row.loc["Customer_Role"] == 'Customer':
                retail += int(row.loc["Order_Total_Amount"])
            else: wholesale += int(row.loc["Order_Total_Amount"])
        sum_sales = retail + wholesale
        counts = self.csv["Customer_Role"].value_counts().to_dict()
        roles = list(counts.keys())
        count = list(counts.values())
        data = zip(roles, count)
        c_role_dataframe = pd.DataFrame(data, columns = ['Roles', 'Count'])
        c_role_dataframe = c_role_dataframe[c_role_dataframe.Roles != 'Subscriber']
        c_role_dataframe.insert(2,column ='Sales_Total', value=[int(retail), int(wholesale)])
        c_role_dataframe['Average_Sale_Revenue']= c_role_dataframe['Sales_Total']/c_role_dataframe['Count']
        c_role_dataframe['Proportional_Sales'] = c_role_dataframe['Sales_Total']/sum_sales
        c_role_dataframe['Proportional_Count'] = c_role_dataframe['Count']/sum_count
        cdb_dv = ColumnDataSource(c_role_dataframe)
        roles = c_role_dataframe['Roles'].tolist()
        cdb_dv.data.keys()
        subkey_list = ['Proportional_Sales', 'Proportional_Count']
        visual = figure(x_range= roles, width=700, height=700,
                        title='Customer Role Sales Breakdown', x_axis_label='Roles',
                        y_axis_label='Proportionate Value', toolbar_location=None, tools='hover',
                        tooltips=[('Average Sale Revenue', '@Average_Sale_Revenue'),
                                  (Proportionate)]
                        )
        visual.vbar_stack(subkey_list, x='Roles', width=0.6, color=['green', 'yellow'],
                          source=cdb_dv, legend_label=subkey_list)
        show(visual)
        return print(c_role_dataframe)

    def geographical_breakdown(self):
        self.csv = self.csv[self.csv.Country_Name_Shipping== 'United States (US)']
        counts = self.csv["State_Name_Shipping"].value_counts().to_dict()
        States = list(counts.keys())
        Count = list(counts.values())
        geo = pd.DataFrame({'States': States, 'Counts': Count})
        geo_dataframe = pd.DataFrame(geo)
        geo_dataframe.insert(loc=2, column="Sales_Total", value=0)
        geo_dataframe.insert(loc=3, column="Avg_Purchase_Revenue", value=0)
        for i, row in self.csv.iterrows():
            state = row.loc['State_Name_Shipping']
            total = row.loc['Order_Total_Amount']
            idx = geo_dataframe[geo_dataframe["States"] == state].index.item()
            av = int(geo_dataframe.at[idx, 'Sales_Total']) / int(geo_dataframe.at[idx, 'Counts'])
            geo_dataframe.at[idx, 'Sales_Total'] += total
            geo_dataframe.at[idx, 'Avg_Purchase_Revenue'] = av
        # data visualization
        cds = ColumnDataSource(geo_dataframe)
        cds.data.keys()
        visual = figure(tools='box_zoom, pan, reset',
                        width=700, height=700,
                        title='Geographical Sales Breakdown',
                        y_axis_label='Order Quantity', x_axis_label='Revenue')
        visual.circle('Sales_Total', 'Counts', size=7, source=cds, name= 'States')
        visual.add_tools(HoverTool(tooltips=[("State", "@States"),
                                             ("Average Purchase Revenue", "@Avg_Purchase_Revenue")
                                             ]))
        show(visual) # If this visualization doesn't work, check out the FIFA Jupyter notebook
        return print(geo_dataframe)


