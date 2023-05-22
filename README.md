# Stereolithography (SLA) PCB manufacturing

This is a simple guide (and a reference for me in the future) to make simple PCBs at home. Other than the actual materials used for the synthesis, only a resin printer is required.

# Stereolithography

Stereolithography (SLA) is an additive manufacturing process commonly used in 3D printing. It is a technique that creates three-dimensional objects by selectively curing layers of liquid photopolymer resin using focused UV light.

Stereolithography is a broad term that encompasses various technologies. Some common SLA variations are:

1. Laser SLA (LSLA): Laser SLA printers use a UV laser as the light source to selectively cure the liquid resin. The laser beam is controlled by mirrors that direct it onto the resin surface, solidifying one point at a time to create each layer.

2. Digital Light Processing (DLP): DLP-based SLA printers use a digital light projector to project an entire layer of the object at once onto the liquid resin. The projected light cures the resin layer by layer. DLP technology typically utilizes a digital micromirror device (DMD) to control the light projection.

3. Masked Stereolithography (MSLA): MSLA printers, also known as LCD-based SLA printers, employ an LCD screen as a mask between the light source and the resin tank. The LCD screen displays the pattern of each layer, selectively allowing UV light to pass through and cure the resin.

4. Continuous Liquid Interface Production (CLIP): CLIP technology utilizes a combination of UV light and oxygen to selectively cure the resin continuously. A transparent window separates the liquid resin from a reservoir of oxygen. The UV light triggers the curing process at the interface between the liquid resin and oxygen, resulting in continuous printing without the need for layer-by-layer processing.

MSLA technology has gained popularity due to its cost-effectiveness. We will use a standard MSLA printer. My MSLA printer is an Anycubic Photon Mono.
Instead of curing resin, we will use the same physical principle to cure a photosensitive film applied over a copper clad, in order to produce a mask that prevent an etching solution to affect certain areas of the board.

# Convert the PCB to a printable file

Most EDAs let you directly export the 3D model of the PCB but sometimes this feature is either paid or not implemented at all (easyEDA at the time I'm writing this). A 3D model of the traces is required for the procedure. For this reason I wrote a simple script that lets you convert a black and white image (or a pdf) to an STL file by extruding the black pixels.

Mirror the STL vertically otherwise the resulting PCB will be upside down and you will not be able to solder the components on it. 

# Copper clad preparation

The first thing to do is clean the copper clad. I usually rub the board with fine grain sanding paper (320-400 grit) to even the surface and remove the stains; do not overdo it because the copper film is thin and could wear out too much, making the traces too thin and brittle; a few strokes with steel wool might help but it is not essential. After the board is clean cut it to proper size. Mark the dimensions and score the surface about 20/30 times with the blunt edge of the cutter on both sides; 

The cutting and sanding contaminates the board with dust and fine bits of copper, the handling of the boards deposits oil from your fingers. Before continuing I usually wipe the surface with alcohol.

Apply the photosensitive film and then heat the board to make the film adhere to the copper: you can apply it by hand and then use an iron (not directly in contact with the film, for example you can use greaseproof paper; be careful not to over heat it or the film will simply melt) or use a laminating machine. I's crucial that the surface has no bubbles, otherwise those areas will not correctly adhere on the copper nor develop and the traces underneath them will be ruined.

# Expose the copper clad

Send the 3D file to your slicer and adjust the exposure of the first layer to 25 seconds and the exposure for the other layers to 0. I found that this works pretty well for me, fine tune the first layer exposure time to suit your needs. These values may vary based on the printer, the photosensitive film and numerous other factors.
Exposing the copper clad for too long will cause the film to develop over a larger area and the result will be too inaccurate.
Exposing the board for too little will cause it not to develop enough.

Place the copper clad in the middle of the LCD screen of the MSLA printer and run start the print process. The masked UV rays will develop the photosensitive film in some areas leaving others protected. The developed photosensitive film will prevent the etching agent to etch the area underneath.

# Etch it 

The plate is then completely submerged in a solution that eats away at the exposed metal. Ferric chloride may be used for etching copper plates as well as zinc plates.
Typical solutions are 1 part FeCl3 to 1 part water. The strength of the acid determines the speed of the etching process.

Shake the tray containing the ferric chloride and the board until only the areas covered by the developed photosensitive film are left.

# Postprocessing

<TODO>
<Place the board in another tray containing>

Check all the traces with a multimeter and score the board with the currer to remove unwanted connections. Done.

This procedure is very simple and lets you prototype fast with new designs without the hassle of waiting for a professionally made pcb to be manufactured and shipped.
