import urllib.request, json, time, simplekml

kml = simplekml.Kml()
print('start')

pnt = kml.newpoint(name="Aircraft", description="Generic aircraft",
                coords=[(18.432314,-33.988862)])  # lon, lat, alt
pnt.altitudemode = simplekml.AltitudeMode.relativetoground #altitude


while True:
    # some JSON:
    with urllib.request.urlopen("http://127.0.0.1:56781/mavlink/") as url:
        y = json.load(url)

    pnt.coords=[(y["GPS_RAW_INT"]["msg"]["lon"] * 0.0000001, y["GPS_RAW_INT"]["msg"]["lat"] * 0.0000001, y["GPS_RAW_INT"]["msg"]["alt"] * 0.001) ]  # lon, lat optional height
    print(y["GPS_RAW_INT"]["msg"]["lon"] * 0.0000001, y["GPS_RAW_INT"]["msg"]["lat"] * 0.0000001, y["GPS_RAW_INT"]["msg"]["alt"] * 0.001) #serial print
    kml.save("pyout.kml")#update kml




    time.sleep (1)











 



