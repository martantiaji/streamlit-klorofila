import streamlit as st
import ee
import geemap
import pandas as pd

service_account = 'chlorophyll51s@tugasakhir-2022.iam.gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, 'tugasakhir-2022-941e93fe6bb1.json')
ee.Initialize(credentials)

def L8_T1():
    
    st.header("Konsentrasi Klorofil-a Landsat 8 Surface Reflectance Tier 1")
    
    st.markdown("![](https://i.postimg.cc/rsLHWRPL/legenda-2.png)")

    start_year = 2013
    end_year = 2020
    study_area = ee.Geometry.Polygon([
        [121.731876,-2.330221], [121.069735, -2.317823], [121.214026,-2.994612], [121.785511,-2.992766]
    ])

    collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR') \
        .filterBounds(study_area)

    yearlist = range(start_year, end_year)


    def mask_clouds(image):
        # Bits 3 and 5 are cloud shadow and cloud, respectively.
        cloud_shadow_bit_mask = (1 << 3)
        clouds_bit_mask = (1 << 5)
        # Get the pixel QA band.
        qa = image.select('pixel_qa')
        # Both flags should be set to zero, indicating clear conditions.
        mask = qa.bitwiseAnd(cloud_shadow_bit_mask).eq(0) \
            .And(qa.bitwiseAnd(clouds_bit_mask).eq(0))
        return image \
            .divide(10000) \
            .divide(3.141593) \
            .updateMask(mask)


    def calculate_clorophil_a(year) :
        image = collection \
            .filter(ee.Filter.calendarRange(year, year, 'year')) \
            .map(mask_clouds) \
            .median()
        ndwi = image \
            .normalizedDifference(['B3', 'B5']) \
            .rename('NDWI')
        clorophil_a = image \
            .expression('10**(-0.9889*((RrsB4)/(RrsB5))+0.3619)', {
                'RrsB4': image.select('B4'),
                'RrsB5': image.select('B5')
            }) \
            .updateMask(ndwi)
        return clorophil_a.clip(study_area)\
            .set('year', year) \
            .set('month', 1) \
            .set('date', ee.Date.fromYMD(year,1,1)) \
            .set('system:time_start',ee.Date.fromYMD(year, 1, 1))

    clorophil_a_collection = ee.ImageCollection.fromImages([
        calculate_clorophil_a(year)
        for year in yearlist
    ])
    print(clorophil_a_collection.getInfo())

    parameter = {'min':0, 'max':1, 'palette':['blue','green']}
   
    m = geemap.Map()
    m.addLayer(clorophil_a_collection,parameter,"Klorofil-a")
    # ################################################################
    # ##################  Show Every Image  ##########################
    # ################################################################
    m.addLayer(clorophil_a_collection.filterDate('2013-01-01','2013-12-31'),parameter,"Klorofil-a 2013")
    m.addLayer(clorophil_a_collection.filterDate('2014-01-01','2014-12-31'),parameter,"Klorofil-a 2014")
    m.addLayer(clorophil_a_collection.filterDate('2015-01-01','2015-12-31'),parameter,"Klorofil-a 2015")
    m.addLayer(clorophil_a_collection.filterDate('2016-01-01','2016-12-31'),parameter,"Klorofil-a 2016")
    m.addLayer(clorophil_a_collection.filterDate('2017-01-01','2017-12-31'),parameter,"Klorofil-a 2017")
    m.addLayer(clorophil_a_collection.filterDate('2018-01-01','2018-12-31'),parameter,"Klorofil-a 2018")
    m.addLayer(clorophil_a_collection.filterDate('2019-01-01','2019-12-31'),parameter,"Klorofil-a 2019")
    m.addLayer(clorophil_a_collection.filterDate('2020-01-01','2020-12-31'),parameter,"Klorofil-a 2020")
    m.add_colorbar(
        parameter,
        label="Klorofil-a (mg/m3)",
        orientation="horizontal",
        layer_name="Klorofil-a",
        transparent_bg=True)
    m.centerObject(study_area, 10)
    m.to_streamlit()

    col12, col22 = st.columns([3, 1])
    col12.subheader("Timelapse Klorofil-a")
    col12.markdown("![Timelapse Chlorophyll-a Tier 1](https://media.giphy.com/media/Lq2dG9Q3H6zLBIAQed/giphy.gif)")
    
    col22.subheader("Tabel Nilai Klorofil-a")
    data= pd.read_csv('ee-chart.csv')
    df=pd.DataFrame(data=data)
    col22.table(df)

    st.subheader("Line Plot Klorofil-a")
    st.markdown("![](https://i.postimg.cc/fbVjYgxr/lineplot.png)")

    #col22.markdown("![Timelapse Chlorophyll-a Tier 2](https://media.giphy.com/media/IdjzI6SLP8kDW46XgZ/giphy.gif)")


def app():
    st.title("Klorofil-a")

    st.markdown("""

    Aplikasi Web ini dibuat dengan menggunakan Streamlit untuk menampilkan nilai 
    estimasi konsentrasi klorofil-a pada Danau Matano dan Danau Towuti. Nilai estimasi konsentrasi klorofil-a menggunakan satuan µg/l. Algoritma yang digunakan juga menggunakan 
    algoritma Jaelani 2015 berdasarkan jurnal [Pemetaan Distribusi Spasial Konsentrasi Klorofil-A dengan Landsat 8 di Danau Matano dan Danau Towuti, Sulawesi Selatan](http://lipi.go.id/publikasi/pemetaan-distribusi-spasial-konsentrasi-klorofil-a-dengan-landsat-8-di-danau-matano-dan-danau-towuti-sulawesi-selatan/2062)

    """)
    
    apps = ["Landsat 8 Surface Reflectance Tier 1", "Landsat 8 Surface Reflectance Tier 2"]
    
    selected_app = st.selectbox("Pilih Citra", apps)
    
    if selected_app == "Landsat 8 Surface Reflectance Tier 1":
        L8_T1()
