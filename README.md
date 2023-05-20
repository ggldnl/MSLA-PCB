# Stereolithography (SLA) PCB manufacturing

This is a simple guide (and a reference for me in the future) to make simple PCBs at home. Other than the actual materials used for the synthesis, only a resin printer is required.

# Convert the PCB to a printable file

Most EDAs let you directly export the 3d model of the PCB but sometimes this feature is either paid or not implemented at all (easyEDA at the time I'm writing this). A 3d model of the traces is required for the procedure. For this reason I wrote a simple script that lets you convert a black and white image (or a pdf) to an STL file by extruding the black pixels.

Mirror the STL vertically otherwise the resulting PCB will be upside down and you will not be able to solder the components on it. 

# Stereolithography

what is it

When selecting the resin, adjust the exposure of the first layer to 25 seconds and the exposure for the other layers to 0; I found that this works pretty well for me, fine tune the first layer exposure time to suit your needs. 
Exposing the copper clad for too long will
Exposing it for too little will

# Copper clad preparation

The first thing to do is clean the copper clad. I usually rub the board with fine grain sanding paper (320-400 grit) to even the surface and remove the stains; do not overdo it because the copper film is thin and could wear out too much, making the traces too thin and brittle; a few strokes with steel wool might help but it is not essential. After the board is clean cut it to proper size. Mark the dimensions and score the surface about 20/30 times with the blunt edge of the cutter on both sides; 

The cutting and sanding contaminates the board with dust and fine bits of copper, the handling of the boards deposits oil from your fingers. Before continuing I usually wipe the surface with alcohol.

Apply the photosensitive film and then heat the board to make the film adhere to the copper: you can apply it by hand and then use an iron (not directly in contact with the film, for example you can use greaseproof paper; be careful not to over heat it or the film will simply melt) or use a laminating machine. I's crucial that the surface has no bubbles, otherwise those areas will not correctly adhere on the copper nor develop and the traces underneath them will be ruined.

# Expose the copper clad

# Etch it 

# Postprocessing

Check all the traces with a multimeter and score the board with the currer to remove unwanted connections. Done.

This procedure is very simple and lets you prototype fast with new designs without the hassle of waiting for a professionally made pcb to be manufactured and shipped.
