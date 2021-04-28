# Model Interferometry | Lab-Session #4

**[Return to Lab Data](https://github.com/PanosEconomou/advanced-lab/tree/main/3.Interferometry/1.Lab-Data)**\
**[Return to Main](https://github.com/PanosEconomou/advanced-lab)**

This is a digital lab notebook entry for the Model Interferometry Lab

## Objectives

The Main objectives of this lab session are as follows.

1. Build a Mach Zehnder interferometer
2. Understand Quantum Gates
3. Do a step by step analysis of pass through pobabilities
4. Build a Hadamard Gate

---

## Methodology

### Build a Mach Zehnder interferometer

We kept the setup of two stirring mirrors directing the laser, as described in previous lab sessions. Then we added a beam splitter and observed the ouptput with two photodetectors. The output of the detectors was connected directly to an oscilloscope. The setup is shown below:

//add picture 

The detector output showed different intensitites for the two beams (passed and reflected). To test if this is an issue with the detectors we tried swapping them and checking if for one beam they give the same signal. We concluded that both detectors indeed give the same output for the same choice of resistance setting.

We concluded that the beam splitter we were using is not a 50-50 beam splitter. We then tested all the beam splitters available and none of them was a 50-50 splitter. 

We also noticed that if we change the resistance of the photodetectors the signals do overlap, concluding that the beam splitters are 40-60.

### Alignment Procedure

To align the interferometer we followed the procedure below. We spent two sessions attempting to do the alignment with three different arm sizes until we finally made it work.  Figure -- shows the final alignment.

1. Align mirror 1 - fix position on table and angle of mirror
    1.1. We need the reflected laser beam to be parallel to the line that the holes in the optical table define, so that at the beam is centred when it enters the interferometer.
    1.2. To do that
    Screw the stand in position such that the laser beam hits the center of the mirror and reflects along the vertical line defined with the holes in the optical table.
2. Align mirror 2
3. 