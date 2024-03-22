import simplekml
kml = simplekml.Kml()
ls = kml.newlinestring(name='A LineString')
ls.coords = [(18.333868,-34.038274,10.0), (18.370618,-34.034421,10.0)]
ls.extrude = 1
ls.altitudemode = simplekml.AltitudeMode.relativetoground
ls.lookat.gxaltitudemode = simplekml.GxAltitudeMode.relativetoseafloor
ls.lookat.latitude = -34.028242
ls.lookat.longitude = 18.356852
ls.lookat.range = 3000
ls.lookat.heading = 56
ls.lookat.tilt = 78
kml.save("LookAt.kml")
