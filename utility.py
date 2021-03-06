import pandas as pd
import os
import customer_profile as cpm
def clean(inp):
    obj = inp
    obj.columns = obj.columns.str.replace(' ','_')
    obj.columns = obj.columns.str.replace('(', '')
    obj.columns = obj.columns.str.replace(')', '')
    obj.fillna(0)
    return obj
# make a concatenate functions
def concat(dir_name):
    frame = pd.DataFrame()
    abs_file_path = os.path.abspath(dir_name)
    for file in os.listdir(abs_file_path):
        if file.endswith('.csv'):
            frame.concat(pd.read_csv(file))
    return frame
            
class FieldLoader:
    def __init__(self, frame):
        self.frame = frame
        self.row_number = 0
        self.gen_wrapper()

    def gen_wrapper(self):
        for i in range(len(self.frame.index)):
            self.row_number = i
            final_list = self.gen_fields()
            init_SalesRow = cpm.SalesRow(*final_list)
            init_SalesRow

    def gen_fields(self):
        #how about making this a list of lists, and making each row accessible as the fields
        # of a customer_profile_module.SalesRow call
        name = self.frame.loc[:, 'Full_Name_Shipping']
        role = self.frame.loc[:, "Customer_Role"]
        email = self.frame.loc[:, 'Email_Billing']
        date = self.frame.loc[:, 'Order_Date']
        first_order = self.frame.loc[:, 'Customer_first_order_date']
        sale_total = self.frame.loc[:, "Order_Total_Amount"]
        number_of_sales = self.frame.loc[:, 'Customer_Total_Orders']
        raw_sales_product_cell = self.frame.loc[:, "Product_Name"]
        raw_product_quantity_cell = self.frame.loc[:, "Quantity"]
        total_gross_sales = self.frame.loc[:, "Customer_Total_Spent"]
        raw_item_cost_cell = self.frame.loc[:, "Item_Cost"]
        field_zip = zip(name, role, email, date, first_order, sale_total, number_of_sales, raw_sales_product_cell,
            raw_product_quantity_cell, raw_item_cost_cell, total_gross_sales)
        return list(field_zip)[self.row_number]

def date_difference_compiler():
    retail = os.listdir(os.getcwd()+'\\retail_customers')
    wholesale = os.listdir(os.getcwd()+'\\wholesale_customers')
    full_set =[]
    day_threshold = 40 # This number will control the days since previous sale threshold for email campaigns
    for i in retail, wholesale:
        c = pd.read_csv('.\\retail_customers\\'+i)
        name = c.at[0,'Value']
        email = c.at[1, 'Value']
        dd_count = c.at[5, 'Totals']
        dd_count =dd_count.split('\n')
        print(dd_count)
        print(type(dd_count))
        if type(dd_count)!= list:
            if int(dd_count) > day_threshold:
                full_set.append(email)
        if type(dd_count) == list:
            if int(dd_count[-1])> day_threshold:
                full_set.append(email)
        print(dd_count)
    for i in wholesale:
        c = pd.read_csv('.\\wholesale_customers\\' + i)
        name = c.at[0, 'Value']
        email = c.at[1, 'Value']
        dd_count = c.at[5, 'Totals']
        dd_count.split('\n')
        print(dd_count)
        print(type(dd_count))
        if type(dd_count) != list:
            if int(dd_count) > day_threshold:
                full_set.append(email)
        if type(dd_count) == list:
            if int(dd_count[-1]) > day_threshold:
                full_set.append(email)
        print(dd_count)
    return print(full_set)
