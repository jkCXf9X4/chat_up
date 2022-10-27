# https://stackoverflow.com/questions/2846947/get-screenshot-on-windows-with-python


# mss 
# https://stackoverflow.com/questions/70370677/can-i-get-the-screenshot-data-as-a-file-like-object-or-the-image-in-bytes-withou
# import mss
# import mss.tools


# with mss.mss() as sct:
#     # The monitor or screen part to capture
#     monitor = sct.monitors[1]  # or a region

#     # Grab the data
#     sct_img = sct.grab(monitor)

#     # Generate the PNG
#     png = mss.tools.to_png(sct_img.rgb, sct_img.size)


# wx python
# https://wiki.wxpython.org/WorkingWithImages#A_Flexible_Screen_Capture_App
# import wx
# app = wx.App()  # Need to create an App instance before doing anything
# screen = wx.ScreenDC()
# size = screen.GetSize()
# bmp = wx.Bitmap(size[0], size[1])
# mem = wx.MemoryDC(bmp)
# mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
# del mem  # Release bitmap
# bmp.SaveFile('screenshot.png', wx.BITMAP_TYPE_PNG)