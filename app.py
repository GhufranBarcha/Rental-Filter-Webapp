import pandas as pd
import gradio as gr

# Load the data from the Excel file
file_path = 'Price_Drop.xlsx'
df = pd.read_excel(file_path)
df["percentage_change"] = abs(df["percentage_change"].str.replace("%", "", regex=False).astype(float))

def search_houses(
    beds, baths, sqft_choice, sqft_value, neighborhood_name, price_choice, price_value,
    price_per_sqft_max, percentage_threshold, concession_applied
):
    # Filter by beds and baths
    filtered_df = df[df['beds'].isin(beds) & df['baths'].isin(baths)]
    
    # Filter by neighborhoods
    if neighborhood_name:
        filtered_df = filtered_df[filtered_df['neighborhood_name'].isin(neighborhood_name)]
    
    # Handle the square footage choice
    if sqft_choice == "Higher":
        filtered_df = filtered_df[filtered_df['sqft'] > sqft_value]
    elif sqft_choice == "Lower":
        filtered_df = filtered_df[filtered_df['sqft'] < sqft_value]
    else:  # "Around"
        filtered_df = filtered_df[(filtered_df['sqft'] >= sqft_value - 300) & (filtered_df['sqft'] <= sqft_value + 300)]
    
    # Handle the price choice
    if price_choice == "Higher":
        filtered_df = filtered_df[filtered_df['net_price'] > price_value]
    elif price_choice == "Lower":
        filtered_df = filtered_df[filtered_df['net_price'] < price_value]
    else:  # "Around"
        filtered_df = filtered_df[(filtered_df['net_price'] >= price_value - 500) & (filtered_df['net_price'] <= price_value + 500)]
    
    # Filter by max price per square foot
    filtered_df = filtered_df[filtered_df['price_per_sqft'] <= price_per_sqft_max]

    # Filter by percentage change threshold
    filtered_df = filtered_df[filtered_df['percentage_change'] >= percentage_threshold]

    # Apply concession filter only if checkbox is selected
    if concession_applied:
        filtered_df = filtered_df[filtered_df['concession_applied'] == True]
    
    return len(filtered_df), filtered_df

# Define the Gradio interface
iface = gr.Interface(
    fn=search_houses,
    inputs=[
        gr.CheckboxGroup(label="Beds", choices=[0, 1, 2, 3, 4], value=[0, 1, 2, 3, 4]),
        gr.CheckboxGroup(label="Baths", choices=[0.0, 1.0, 1.5, 2.0, 2.5, 3.0], value=[0.0, 1.0, 1.5, 2.0, 2.5, 3.0]),
        gr.Radio(label="Square Feet Choice", choices=["Higher", "Lower", "Around"], value="Higher"),
        gr.Number(label="Square Feet Value", value=329, minimum=329, maximum=3249),
        gr.Dropdown(label="neighborhood_name", choices=[
            "South Loop", "River North", "West Loop", "Streeterville", "The Loop", 
            "Old Town", "Gold Coast", "New East Side", "Old town", "Lincoln Park", 
            "Fulton River District", "Bronzeville", "Lake View", "River West", 
            "Buena Park", "Fulton Market", "Goose Island", "Near North Side", 
            "Ravenswood", "Uptown", "Logan Square", "East Hyde Park", "Wicker Park", 
            "Hyde Park", "Rogers Park", "Near South Side", "Edgewater Beach", "Cragin"
        ], value=["South Loop"], multiselect=True),  # Enable multiple neighborhood selection
        gr.Radio(label="Price Choice", choices=["Higher", "Lower", "Around"], value="Higher"),
        gr.Number(label="Price Value", value=919, minimum=919, maximum=13468),
        gr.Number(label="Max Price per Sqft", value=5.8, minimum=1.429, maximum=5.861),
        gr.Number(label="Percentage Threshold", value=0, maximum=df["percentage_change"].max()),
        gr.Checkbox(label="Concession Applied")
    ],
    outputs=[
        gr.Text(label= "Sample Count"),
        gr.Dataframe(label="Filtered DataFrame" ,height= 400)
    ],
    title="Comprehensive House Search App",
    description="Search for houses based on various criteria and view the results in a table."
)

# Launch the app
iface.launch()
