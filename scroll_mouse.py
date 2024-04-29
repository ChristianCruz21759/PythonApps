# imageDim - volume of the dicom files
 
root = tkinter.Tk()
root.wm_title("Try MouseWheel")
slide = 128
minInt = np.min(imageDim)
maxInt = np.max(imageDim)
def main_loop():
 
    fig, ax = plt.subplots()
    ax.imshow(imageDim[:, :, slide], cmap='gray', vmin=minInt, vmax=maxInt, zorder=1)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand='true')
    canvas.mpl_connect('scroll_event', mouse_wheel)
 
def mouse_wheel(event):
    global slide
    fig = event.canvas.figure
    ax = fig.axes[0]
    print(slide)
    print(event.step)
 
    if event.step < 0:
        slide += event.step
        ax.imshow(imageDim[:, :, int(slide)], cmap='gray', vmin=minInt, vmax=maxInt, zorder=1)
 
    if event.step > 0:
        slide += event.step
        ax.imshow(imageDim[:, :, int(slide)], cmap='gray', vmin=minInt, vmax=maxInt, zorder=1)
    fig.canvas.draw()
 
 
main_loop()
root.mainloop()