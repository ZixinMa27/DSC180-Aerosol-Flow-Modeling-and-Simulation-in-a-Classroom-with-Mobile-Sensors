## Modeling and Simulation of Aerosol Flow with Mobile Sensors
## Introduction
**Motivation**:
Indoor air quality is very important when it comes to ensuring the safety and comfort of individuals in a variety of settings. However, the existing air quality monitoring systems are often costly and do not fully consider risks assoiated with respiratory droplets and aerosols. Therefore, a tool that can provide information regarding the duration of exposure to resporatory aerosols would prove to be incredibly beneficial. By utilizing such a tool, individuals and organizations would be better equipped to make informed decisions regarding the safety of indoor environments, thereby minimizing the risk of respiratory infections and promoting overall health and well-being.

**Goals**:
In this project, we aim to develop application to monitor resident time of human respiratory aerosols in indoor environment utilizing mobile sensors and machine learning models, with the aim of improving the safety of people, especially in high-risk environment such as hospitals, healthcare facilities, and classrooms. The app will capture syndromic signal such as cough and provide dinformation to optimize safety in dynamic real world setting and use cost effective and accessible to the general public.

## Methods
The project is divideed into three stages: **Data collection**, **Data Visualization**, and **Modeling and Simulation**.
### Data Collection 
#### Data Collection APP Development
We developed an iOS application for collection of data and proof of concept deployment of models. <br>
Our app includes features such as: 
* **Audio**: capture and classify audio to detect human respiratory events such as cough, sneeze
* **Thermal Image**: using a FLIR one camera to detect surface temperatures, and detect human presence, and movement in the thermal image using YOLO model
* **Lidar and Camera**: capture room layout info and geomtry required for modeling and CFD simulation
* **Database**: store collected data online using Firebase

<table><tr>
<td> <img src="assets/app_view.png"  width= "300"/> </td>
<td> <img src="assets/thermal_audio.png" width= "300"/> </td>
<td> <img src="assets/app_scan_view.png" width= "300"/> </td>
<p align = "center">
APP Content View
</p>
</tr></table>


<iframe width="800" height="450" src="https://youtu.be/embed/suGByOBXNN8" title="APP demo" frameborder="0" allowfullscreen></iframe>

#### Tools for Measuring Aerosol Concentrations

<table align="center">
  <tr>
    <td>
        <img style="width: 300px; height: 200px" src='assets/SPS30.png' />
     </td>
     <td>
     <figcaption style="width: 400px">We used the SPS30 Particulate Matter Sensor to measure our ground truth aerosol concentration. </figcaption>
     </td>
  </tr>
</table>

#### Data Collection Process
<table><tr>
<td>
<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.0.1/model-viewer.min.js"></script>
<style>
model-viewer {
  width: 380px;
  height: 400px;
}
</style>
<model-viewer alt="Model of Data Collection Room Setting Produced from LiDAR" src="assets/Uc302.gltf" ar shadow-intensity="1" camera-controls touch-action="pan-y">
</model-viewer>
</td>
<td> <figcaption style="width: 400px">We established a test environment in a compact office space (approx. dimenisions - 3.2m, 2.6m, 3.2m), where we mechanically simulated human coughs and captured aerosol concentrations using particulate matter (PM) sensors.</figcaption>
</td>
</tr></table>


<table align="center">
  <tr>
    <td>
        <img style="width: 400px; height: 350px" src='assets/fog_machine.png'/>
     </td>
     <td>
     <figcaption style="width: 400px">The cough simulation involved a mannequin, mechanical ventilator, fog machine, and air compressor.</figcaption>
     </td>
  </tr>
</table>

<table align="center">
  <tr>
    <td>
        <img style="width: 400px; height: 350px" src='assets/room_layout.png'/>
     </td>
     <td>
     <figcaption style="width: 400px"> We have installed six PM sensors to measure the actual particle concentration in the room. The location of each sensor is indicated in the layout.</figcaption>
     </td>
  </tr>
</table>

<table align="center">
  <tr>
    <td>
        <img style="width: 400px; height: 350px" src='assets/tripod.png'/>
     </td>
     <td>
     <figcaption style="width: 400px" >The iPhone is mounted on a tripod in front of a mannequin to capture thermal images and audio. In the picture, three sensors can be seen: one directly in front of the mannequin, one positioned on the tripod with the iPhone, and another located on the side of the wall close to the door. These sensors are used to measure aerosol concentrations.</figcaption>
     </td>
  </tr>
</table>
<table align="center">
  <tr>
    <td>
        <img style="width: 400px; height: 350px" src='assets/exhaust.png' />
     </td>
     <td>
     <figcaption style="width: 400px">The fan machine is located in the right back corner, which we refer to as the exhaust area, and one sensor is positioned there to measure aerosol concentrations. Another sensor is placed on the wall behind the mannequin.</figcaption>
     </td>
  </tr>
</table>
<table align="center">
  <tr>
    <td>
        <img style="width: 400px; height: 350px" src='assets/mannequin.png' />
     </td>
     <td>
     <figcaption style="width: 400px">Our data collection app, which we have developed for this purpose, allows us to capture thermal images of the room using a thermal camera. In the image, the temperature of the mannequin is shown as 46.5 degrees Celsius, due to the heat generated by the fog machine.</figcaption>
     </td>
  </tr>
</table>


### Data visualization

#### Exploratory Data Analysis 
Our exploratory data visualization has revealed that the dispersion and duration of aerosol concentrations at various sensor locations varies under different fan speed settings during a cough event. 

<table>
<caption>Impact of Fan Speed and Sensor Location on Aerosol Concentrations </caption>
<tr>
<td> {% include pm2p5_data_low_speed.html %}  </td>
<td> {% include pm2p5_data_medium_speed.html%} </td>
</tr>
</table>
<table>
<tr>
<td> {% include pm2p5_data_high_speed.html%} </td>
<td> {% include pm2p5_data_no_ac.html%} </td>
</tr>
</table>

To better illustrate these differences, we used a log scale graph and an aerosol concentration at exhaust location graph for comparison. 

<table align="center">
  <tr>
    <td>
        <img style="width: 400px; height: 350px" src='assets/PM2.5_Diff_Loc.png' />
        <img style="width: 400px; height: 350px" src='assets/conc_exhuast.png' />
     </td>
     <td>
     <figcaption style="width: 400px"> Observation: In the absence of air conditioning, aerosols tend to persist in a room for a longer time and disperse and disappear at a slower rate than when the fan is turned on. Furthermore, under high-speed fan settings, aerosol concentration is lower and disperses faster than under low-speed settings. This suggests that the air exchange rate in the room plays a critical role in the changes in aerosol concentration.</figcaption>
     </td>
  </tr>
</table>


We also conducted experiments under three different room conditions. <br>
1. Leaving the door open during the cough simulation event. 
2. Keeping the door closed during the cough simulation event. 
3. The door was closed during the cough simulation event and then opened afterward. 

Observation: We discovered that air flow also plays a crucial role in the changes in aerosol concentration. When the door is open, the aerosol concentration is significantly lower than when the door is closed, which suggests that the exchange of air with the surrounding environment can help to reduce the concentration of aerosols in the room. Conversely, the resident time for aerosols was longer in enclosed environments.


![image3](/assets/room_condition.png)

The following animation helps to visualize how the aerosol concentration in a room changes after a cough event.

{% include pm_data_animation.html%}

**Significance**: These observations highlight the importance of considering room conditions, such as ventilation and air flow, when developing models to forecast aerosol concentration in different settings. By taking into account the influence of room conditions, we can develop more accurate models and better understand the factors affecting aerosol dispersion.

##  Modeling and Simulations

### Compartment Model
To forecast aerosol concentration, we utilized two compartment models with one sub-compartment. We solved the equation of aerosol concentration in both the perfectly mixed parent compartment (<math><msub><mi>C</mi><mi>p</mi></msub></math>) and subcompartment (<math><msub><mi>C</mi><mi>s</mi></msub></math>) over time. However, for the sake of simplicity, we neglected the sinks (settling) factor and focused solely on the aerosol concentration in the parent compartment. 
<table>
<tr><td>
<table>
  <tr>
    <th>Variable</th>
    <th>Description</th>
  </tr>
  <tr>
    <td> <math><msub><mi>V</mi><mi>p</mi></msub></math></td>
    <td> Volume of parent compartment</td>
  </tr>
  <tr>
    <td><math><msub><mi>V</mi><mi>s</mi></msub></math></td>
    <td> Volume of sub-compartment</td>
  </tr>
  <tr>
    <td><math><mi>Q</mi></math></td>
    <td> Room air exchange rate</td>
  </tr>
  <tr>
    <td><math><msub><mi>C</mi><mi>p</mi></msub></math></td>
    <td> Aerosol concentration in the perfectly mixed parent compartment</td>
  </tr>
  <tr>
    <td><math><msub><mi>C</mi><mi>s</mi></msub></math></td>
    <td> Aerosol concentration in the perfectly mixed sub-compartment</td>
  </tr>
  <tr>
    <td><math><mi>α</mi></math></td>
    <td> Compartment coupling coefficient</td>
  </tr>
  <tr>
    <td><math><mi>t</mi></math></td>
    <td> Time</td>
  </tr>
  <tr>
    <td><math><msub><mi>G</mi><mi>p</mi></msub></math></td>
    <td> Settling rate factor in parent compartment</td>
  </tr>
  <tr>
    <td><math><msub><mi>G</mi><mi>s</mi></msub></math></td>
    <td> Settling rate for factor in sub-compartment</td>
  </tr>
</table> </td>
<td> <img src="assets/model.png" alt="model" width= "400"/> 
<img src="assets/equation.png" alt="model" width= "400"/> </td>
</tr>
</table> 

### Model Prediction
Our predictions of aerosol concentration are heavily influenced by the air exchange rate (<math><mi>Q</mi></math>) and compartment coupling coefficient (<math><mi>α</mi></math>). After researching common air exchange rates for different room settings (as listed on The Engineering Toolbox website) and conducting multiple trials and errors on the coefficient, we were able to determine the best-fit model with varying parameters under different fan speed settings.

<table>
<tr><td>
<table>
  <tr>
    <th>Variable</th>
    <th>Value</th>
  </tr>
  <tr>
    <td> SubCompartment Number </td>
    <td> 1</td>
  </tr>
  <tr>
    <td> <math><msub><mi>V</mi><mi>p</mi></msub></math></td>
    <td> 26.5</td>
  </tr>
  <tr>
    <td><math><msub><mi>V</mi><mi>s</mi></msub></math></td>
    <td> 26</td>
  </tr>
  <tr>
    <td><math><mi>Q</mi></math></td>
    <td> 4</td>
  </tr>
  <tr>
    <td>Initial <math><msub><mi>C</mi><mi>p</mi></msub></math></td>
    <td> 0</td>
  </tr>
  <tr>
    <td>Initial <math><msub><mi>C</mi><mi>s</mi></msub></math></td>
    <td> 0</td>
  </tr>
  <tr>
    <td><math><mi>α</mi></math></td>
    <td> 0.4</td>
  </tr>
  <tr>
    <td><math><mi>t</mi></math></td>
    <td> 200</td>
  </tr>
</table> </td>
<td> <img src="assets/pred_low.png" alt="model" width= "400"/>  
<p>aerosol concentration prediction of at low fan speed setting</p>
</td>
</tr>
</table> 

<table>
<tr><td>
<table>
  <tr>
    <th>Variable</th>
    <th>Value</th>
  </tr>
  <tr>
    <td> SubCompartment Number </td>
    <td> 1</td>
  </tr>
  <tr>
    <td> <math><msub><mi>V</mi><mi>p</mi></msub></math></td>
    <td> 26.5</td>
  </tr>
  <tr>
    <td><math><msub><mi>V</mi><mi>s</mi></msub></math></td>
    <td> 26</td>
  </tr>
  <tr>
    <td><math><mi>Q</mi></math></td>
    <td> 4</td>
  </tr>
  <tr>
    <td>Initial <math><msub><mi>C</mi><mi>p</mi></msub></math></td>
    <td> 0</td>
  </tr>
  <tr>
    <td>Initial <math><msub><mi>C</mi><mi>s</mi></msub></math></td>
    <td> 0</td>
  </tr>
  <tr>
    <td><math><mi>α</mi></math></td>
    <td> 0.4</td>
  </tr>
  <tr>
    <td><math><mi>t</mi></math></td>
    <td> 200</td>
  </tr>
</table> </td>
<td> <img src="assets/pred_hig.png" alt="model" width= "400"/>  
<p>aerosol concentration prediction at high fan speed setting</p>
</td>
</tr>
</table> 

<table>
<tr><td>
<table>
  <tr>
    <th>Variable</th>
    <th>Value</th>
  </tr>
  <tr>
    <td> SubCompartment Number </td>
    <td> 1</td>
  </tr>
  <tr>
    <td> <math><msub><mi>V</mi><mi>p</mi></msub></math></td>
    <td> 26.5</td>
  </tr>
  <tr>
    <td><math><msub><mi>V</mi><mi>s</mi></msub></math></td>
    <td> 26</td>
  </tr>
  <tr>
    <td><math><mi>Q</mi></math></td>
    <td> 4</td>
  </tr>
  <tr>
    <td>Initial <math><msub><mi>C</mi><mi>p</mi></msub></math></td>
    <td> 0</td>
  </tr>
  <tr>
    <td>Initial <math><msub><mi>C</mi><mi>s</mi></msub></math></td>
    <td> 0</td>
  </tr>
  <tr>
    <td><math><mi>α</mi></math></td>
    <td> 0.4</td>
  </tr>
  <tr>
    <td><math><mi>t</mi></math></td>
    <td> 200</td>
  </tr>
</table> </td>
<td> <img src="assets/pred_noa.png" alt="model" width= "400"/>  
<p> aerosol concentration prediction of at no ac setting</p>
</td>
</tr>
</table> 


### Computational Fluid Dynamics Simulation 
Aside from modeling, we also utilized professional simulation software to validate our data collection process, especially the locations where we should put the PM sensors. The software is Ansys Discovery, a computational fluid dynamics simulation tool that can model airflows in an enclosed space. From the figure below, it is clear that when airflow attempts to pass through the different furnitures in the room, the air is likely to be disrupted and form a vortex which can have temporarily increased aerosol concentration in the room. The simulation serves as an extra data source for us to make sure that we are doing things correctly. However, due to our limited knowledge about CFD, the simulation setting still needs some work before being able to simulate actual coughing. As of right now, the software provides us with an opportunity to examine the possible airflow conditions in the test room.

![image6](/assets/discovery_sim.png)


## Conclusion & Discussion
For this project, we have developed models using measured sensor data and simulation data to develop robust models to predict aerosol resident time. In the future, we woill continue work on compartment model and we need a better way to determine the value of alpha and the air exchange rate instead of manually tuning parameters. We will continue to improve the model’s accuracy in incorporating sound labels and subject movement.

## Reference
[1] Rahman, Tauhidur. Modeling indoor Air quality and Aerosol Transport with Simulation Digital Twins, 2022. University of California, San Diego. <br>
[2] The Engineering Toolbox. Air Change Rates in Typical Rooms and Buildings. https://www.engineeringtoolbox.com/air-change-rate-room-d_867.html <br>
[3] A Perez, J Penaloza Gutierrez, A Tejada-Martinez - APS Division of Fluid Dynamics Meeting Abstracts, 2021. Two-compartment modeling of a hospital isolation room informed by CFD <br>
[4] Cough simulator - George Zhou, Garrett W. Burnett, Ronak S. Shah, Cheuk Yin Lai, Daniel Katz, and Eric A. Fried. Development of an Easily Reproducible Cough Simulator With Droplets and Aerosols for Rapidly Testing Novel Personal Protective Equipment. Simulation in Healthcare: The Journal of the Society for Simulation in Healthcare, Publish Ahead of Print, March 2022 <br>
