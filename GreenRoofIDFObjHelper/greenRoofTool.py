


"""
Use this component to create a Material:Roofvegitation input object to hopefully plug into Honeybee_EP construction
_
This component requires ALOT of user input but it was easier for me than inputting IDF text blocks
_
Idk what else to tell ya: go here https://bigladdersoftware.com/epx/docs/8-0/input-output-reference/page-010.html#materialroofvegetation
-
Provided by adderal and coffee

	Args:
		_name: A text name for your roof object.
		_plantHeight: the height of your plants in meters.
		_leafAreaIndex: projected area per unit area of sol surface in the range of 0.001 < LAI < 5.0. default is 1.0.
		_leafReflectivity: fraction of incident solar rad reflected by individual leaf surfaces (albedo) must be between 0.05 and 0.5 default should be .22 typcal val= 0.18..0.25.
		_leafEmissivity: ratio of thermal radiation emitted from leaf surface to that emitted by an ideal black body values should be between 0.8 and 1.0 (1.0 rep black body).
		_minStomatalResi: this field represents the resistance of the plants to moisture transport. it has units of s/m, lower the value higher evapotranspiration rate  values range 50.0 to 300.0 default is 180.
		_soilLayerName: this field is for naming the soil layer.
		_roughness: relative roughness, this influences the convection coefficients specifically exterior convection coef, "VeryRough", "Rough", "MediumRough", ect.
		_thickness: thickness of the material layer in meters, this should be the dimension of the layer in the direction perp to the main path of heat conduction max is .7m must be greater than .05m.
		_conductivityOfDrySoil: W/(m-K) must be greater than 0, typical soils .3-.5 min is .2 max is 1.5.
		_densityOfDrySoil: kg/m2 min 300 max 2000. 
		_specificHeatCapDrySoil: J/(kg-K)  note most refrences may be kj/(kg-K) or J/(g-K) but thats no biggie. THANKS METRIC!! <3.
		_thermalAbsp_: represents the fraction of incident long wave rad absorbed by the material. 0.0-1.0  1.0 = blackBody typical= .9 to .98.
		_solAbsp_: fraction of incident solar rad absorbed by material. if solar reflectance or reflectivity data is avail absorptance is equal to 1.0 minus reflectance (Love when stuff converts amicably) typical val .6 to .85 range is 0.0 and 1.0.
		_visAbsp_: fraction of incident visible wavelength rad absorbed by materia. its diff than solar. same as above 1.0 - reflectance or reflectivity range is 0.5 to 1.0.
		_satVolMoistContOfSL: max moisture content, typically less than .5 range is .1 to .5 typical is .3.
		_resVolMoistContOfSL: residual moisture content of soil layer range .01 to .1 default .01.
		_initVolMoistContOfSL: innit moisture content range .05 to .5 with default .1. 
		_moistDiffCalcMethod: simple or advanced ie constant or vairiable defusion.
	Returns:
		EPMaterial: A hopefully functionable green roof mat fuo HB EP construction component.

"""




ghenv.Component.Name = "GreenRoofGnome"
ghenv.Component.NickName = 'EPGreenOpaqueMat'
ghenv.Component.Message = 'VER 0.0.1\nOCT_11_2020'
ghenv.Component.Category = 'UDTools'
ghenv.Component.SubCategory = "03 | Utility | HB"
# hopefull compat ver HB .65
try: ghenv.Component.AdditionalHelpFromDocStrings = "0"
except: pass

import Grasshopper.Kernel as gh
warn = gh.GH_RuntimeMessageLevel.Warning


def checkInputs():
	# SHGC and VT are between 0 & 1 
	checkData = True

	def checkBtwZeroAndOne(variable, default, variableName): 
		if variable == None: newVariable = default
		else:
			if variable <= 1 and variable >= 0: newVariable = variable
			else:
				newVariable = 0
				checkData = False
				warning = variableName + " must be in certain range, check input hint "
				print warning
				ghenv.Component.AddRuntimeMessage(warn, warning)

		return newVariable

	thermalAbs = checkBtwZeroAndOne(_thermalAbsp_, None, "_thermAbsp_")
	solAbsp = checkBtwZeroAndOne(_solAbsp_, None, "_solAbsp_")
	visAbsp = checkBtwZeroAndOne(_visAbsp_, None, "_visAbsp_")

	#Check the Roughness val 
	if _roughness_ != None: _roughness = roughness_.upper()
	else: _roughness = None
	if _roughness == None or _roughness == "VERYROUGH" or _roughness == "MEDIUMROUGH" or _roughness == "MEDIUMSMOOTH" or _roughness == "SMOOTH" or _roughness == "VERYSMOOTH": pass
	else:
		checkData = False
		warning = "_roughness_ is not valid."
		print warning
		ghenv.Component.AddRuntimeMessage(warn, warning)

	return checkData

def main(name, plantHeight, leafAreaIndex, leafReflectivity, leafEmissivity, minStomatalResi, soilLayerName, roughness, thickness, conductivityOfDrySoil, densityOfDrySoil, specificHeatCapDrySoil, thermalAbsp, solAbsp, visAbsp, satVolMoistContOfSL, resVolMoistContOfSL, initVolMoistContOfSL, moistDiffCalcMethod):

	if plantHeight == None: plantHeight = .2
	if leafAreaIndex == None: leafAreaIndex = 1.0
	if leafReflectivity == None: leafReflectivity = .22
	if leafEmissivity == None: leafEmissivity = .95
	if minStomatalResi == None: minStomatalResi = 180
	if soilLayerName == None: soilLayerName = "NameYaDirtFam"
	if roughness == None: roughness = "MediumSmooth"
	if thickness == None: thickness = .1
	if conductivityOfDrySoil == None: conductivityOfDrySoil = .35
	if densityOfDrySoil == None: densityOfDrySoil = 1100
	if specificHeatCapDrySoil == None: specificHeatCapDrySoil = 1200
	if thermalAbsp == None: thermalAbsp = 0.9
	if solAbsp == None: solAbsp = 0.7
	if visAbsp == None: visAbsp = 0.7
	if satVolMoistContOfSL == None: satVolMoistContOfSL = .3
	if resVolMoistContOfSL == None: resVolMoistContOfSL = .01
	if initVolMoistContOfSL == None: initVolMoistContOfSL = .1
	if moistDiffCalcMethod == None: moistDiffCalcMethod = "Simple" 
	

	values = [name.upper(), plantHeight, leafAreaIndex, leafReflectivity, leafEmissivity, minStomatalResi, soilLayerName, roughness, thickness, conductivityOfDrySoil, densityOfDrySoil, specificHeatCapDrySoil, thermalAbsp, visAbsp, satVolMoistContOfSL, resVolMoistContOfSL, initVolMoistContOfSL, moistDiffCalcMethod]
	comments = ["Name", "Plant Height {m}", "Leaf Area Index {dimensionless}", "Leaf Reflectivity {dimensionless}", "Leaf Emissivity", "Minimum Stomatal Resistance {s/m}", "Soil Layer Name", "Roughness", "Thickness {m}", "Conductivity Of Dry Soil {W/m-K}", "Density of Dry Soil {kg/m3}", "Specific Heat of Dry Soil {J/kg-K}", "Thermal Absorptance", "Solar Absorptance", "Visible Absorptance", "Saturation Volumetric Moisture Content of the Soil Layer", " Residual Volumetric Moisture Content of the Soil Layer", "Initial Volumetric Moisture Content of the Soil Layer", "Moisture Diffusion Calculation Method"]

	materialStr = "Material:Roofvegetation, \n"

	for count, (value, comment) in enumerate(zip(values, comments)):
		if count!= len(values) -1:
			materialStr += str(value) + ",    !- " + str(comment) + "\n"
		else: 
			materialStr += str(value) + ";    !- " + str(comment)

	return materialStr

if _name and _plantHeight and _leafAreaIndex and _leafReflectivity and _leafEmissivity:
	checkData = checkInputs()
	if checkData == True:
		EPMaterial = main(_name, _plantHeight, _leafAreaIndex, _leafReflectivity, _leafEmissivity, _minStomatalResi, _soilLayerName, _roughness_, _thickness, _conductivityOfDrySoil, _densityOfDrySoil, _specificHeatCapDrySoil, _thermalAbsp_, _solAbsp_, _visAbsp_, _satVolMoistContOfSL, _resVolMoistContOfSL, _initVolMoistContOfSL, _moistDiffCalcMethod)