import streamlit as st
from utils import Pipeline
from PIL import Image
import pandas as pd

def main():
    st.title('Diamond Price Recommender 💎')
    st.markdown("""This App generates a price recommendation for your diamond. Just enter the characteristics of the diamond on the left-hand sidebar and then press the button **recommend price**. That's it 🙂.
    """)
 

    # Options for quality, color, clarity
    quality_options = ('Fair', 'Good', 'Very Good', 'Premium', 'Ideal')
    color_options = ('J', 'I', 'H', 'G', 'F', 'E', 'D')
    clarity_options = ('I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF')
    
    help_color_options = 'Values from worst (J) to best (D).'
    help_clarity_options = 'Values from worst (I1) to best (IF).'

    # Side bar
    st.sidebar.title('Enter your diamonds characteristics')
    quality = st.sidebar.select_slider('Quality', options=quality_options,value='Very Good')
    color = st.sidebar.select_slider('Color', options=color_options, value='E', help=help_color_options) 
    clarity = st.sidebar.select_slider('Clarity', options=clarity_options, value='SI1', help=help_clarity_options)
    weight = st.sidebar.number_input('Carat (weight)', min_value=0.0, max_value=5.0, value=0.7)
    st.sidebar.write(f'{weight:.2f} carat = {weight*200:.2f}mg')
    
    st.sidebar.subheader('Dimensions (mm)')
    length = st.sidebar.number_input('Length', min_value=0.0, max_value=12.0, value=5.76)
    width = st.sidebar.number_input('Width', min_value=0.0, max_value=60.0, value=5.7)
    depth = st.sidebar.number_input('Depth', min_value=0.0, max_value=32.0, value=3.43)

    # st.subheader('Vales selected')
    # col1, col2, col3 = st.columns(3)
    # col4, col5, col6, col7 = st.columns(4)
    # col1.metric('Quality', quality)
    # col2.metric('Color', color)
    # col3.metric('Clarity', clarity)
    # col4.metric('Weight', weight)
    # col5.metric('Length', length)
    # col6.metric('Width', width)
    # col7.metric('Depth', depth)

    # Dictionary with all features:
    input_data = {
        'weight': weight,
        'length': length,
        'width': width,
        'depth': depth,
        'quality': quality,
        'color': color,
        'clarity': clarity
    }
    st.write('These are your diamond characteristics:')
    df_inputs = pd.DataFrame(input_data, index=[0])
    st.dataframe(df_inputs)

    # Button to run price prediction
    if st.button('Recommend price'):
        price_prediction = Pipeline(input_data).make_prediction()
        st.write('The recommended price is:')
        st.success(f'$US {price_prediction:.2f}')


    st.subheader('How it works?')
    st.markdown("""
    The price is based on quality, color, clarity, weight, and dimensions. To find out more about how these properties are measured, please check below.
    """)
    with st.expander('See how the characteristics are measured'): 
        tab1, tab2, tab3, tab4, tab5  = st.tabs(['Quality', 'Color', 'Clarity', 'Carat', 'Dimensions'])
        # Tab for quality
        with tab1:
            st.markdown("""
                The quality of a diamond can be classified from best to worst as:
                - Ideal
                - Premium
                - Very good
                - Good
                - Fair
                """)
        # Tab for color
        with tab2:
            st.markdown("""
            The are seven color categories from best to worst: D, E, F, G, H, I.

            For more information about the difference between the colors, please visit: https://www.withclarity.com/education/diamond-education/diamond-color/d-e-f-color-diamonds
            """)

        # Tab for clarity
        with tab3:
            st.markdown("""
            There are different clarities:
            - **IF** (internally flawless) - Only minor surface blemishes but no internal inclusions visible to a trained eye under 10x magnification.
            - **VVS1, VVS2** (very, very slightly included) - Few, very small inclusions and/or finish faults, difficult for a trained eye to see under 10x magnification. Typical flaws include tiny pinpoints, faint clouds, tiny feathers, or internal graining.
            - **VS1, VS2** (very slightly included) - Very small inclusions and/or finish faults, somewhat difficult for a trained eye to see under 10x magnification. Typical flaws include crystals, feathers, distinct clouds and groupings of pinpoints.
            - **SI1, SI2** (slightly included) - Small inclusions and/or surface blemishes are easily seen under 10x magnification, but not visible face-up to a naked trained eye. Typical flaws include crystals, clouds and feathers.
            - **I1** (imperfect 1) - Inclusions and/or finish faults visible under 10x magnification, but hard to see with the naked human eye. Little effect on the brilliance of a stone.

            Source: https://www.aurum.co.nz/guide-to-diamonds/diamond-clarity-explained-nz/
            """)

        # Tab for carat
        with tab4:
            st.markdown("""
            The term *carat* refers to the weight of the diamond. In the international system, one carat equals 200mg (miligrams).
            """)

        # Tab for dimensions
        with tab5:
            st.write('Use the figures as a reference to measure length, width, and depth.')
            col1, col2 = st.columns(2)
            with col1:
                image_length = Image.open('images/length_width.jpeg')
                st.image(image_length, width=300, caption='Example of length and width. Source: https://www.gemsociety.org/article/diamond-measurements/')
            with col2:
                image_depth = Image.open('images/depth.jpeg')
                st.image(image_depth, width=300, caption='Example of length and width. Source: https://www.diamonds.pro/guides/diamond-proportion/')

    


    

