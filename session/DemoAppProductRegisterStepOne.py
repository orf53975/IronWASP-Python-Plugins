#Author: Lavakumar Kuppan
#License: MIT License - http://www.opensource.org/licenses/mit-license

from IronWASP import *
from System import *
import clr

#Inherit from the base SessionPlugin class
class DemoAppProductRegisterStepOne(SessionPlugin):

	#Override the Update method with custom code to check the validity of the Request/Response and update the Request. Returns Request
	def Update(self, Req, Res):
		Req.SetCookie(Res)
		return Req

	#Override the ProcessInjection method to update the Payload before it is injected. Returns String
	def ProcessInjection(self, Scnr, Req, Payload):
		return Payload

	#Override the PrepareForInjection method to make changes to the request or perform other steps before injecting. Returns Request
	def PrepareForInjection(self, Req):
		if Req.Method == "POST" and Req.Url == "/product" and Req.Body.Has("name"):
			#Start the Registration Process
			ResetReq = Request("http://" + Req.Host + "/product/add")
			ResetReq.CookieString = Req.CookieString
			#Since this is an user created Request the Source must be explicitly set
			#Setting this ensures the log is visible under 'Scan Logs'. If this is not done then it will be under 'Shell Logs'
			ResetReq.Source = RequestSource.Scan
			ResetReq.Send()
		return Req

	#Override the GetInterestingResponse method to perform customs actions after the injection is done. Returns Response
	def GetInterestingResponse(self, Req, Res):
		if Req.Method == "POST" and Req.Url == "/product" and Req.Body.Has("name"):
			#Complete StepTwo of registration
			StepTwoReq = Req.GetClone()#cloning the earlier request to get the cookie and other header details
			StepTwoReq.Body.Remove("name")
			StepTwoReq.Body.Set("details","Sample Product Detail")
			StepTwoRes = StepTwoReq.Send()
			
			#Complete StepThree of registration and return final response
			StepThreeReq = Req.GetClone()
			StepThreeReq.Body.Remove("name")
			StepThreeReq.Body.Set("price","123")
			StepThreeRes = StepThreeReq.Send()
			return StepThreeRes
		else:
			return Res

p = DemoAppProductRegisterStepOne()
p.Name = "DemoAppProductRegisterStepOne"
p.Description = "Completes the Product Description and Product Price steps automatically and gets the final response"
SessionPlugin.Add(p)