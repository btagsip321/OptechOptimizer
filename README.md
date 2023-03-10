# Optech Optimizer
A python web application implemented on the Heroku framework, which aims to create optimal PC builds in a streamlined, simple manner for users. This is a capstone project for Project Lead The Way (PLTW).

## Usage

The backbone of the web application uses the buildPc module to calculate the maximum budget for the given PC. This function returns a dictionary of optimal PC builds using metric data for the average percentage used on PC components of most PC builds (The prices are in USD $).
```python
import buildPc
buildPc.buildBudget(1000, True)
```
Output:
```
{
'GPU': 275.4, 
'CPU': 194.4, 
'Windows Key': 100, 
'RAM': 56.7, 
'Case': 45.0, 
'PSU': 74.7, 
'SSD': 45.9, 
'HDD': 41.4, 
'Motherboard': 76.5, 
'CPU Cooler': 26.1, 
'Wifi Adapter': 22.5, 
'Peripherals': 41.4
}
```
After running and deploying the heroku application, you can send a GET request to ./build, which will return a JSONified string of the above function's output.

## Contributing
This is a personal school project, and as such public contributions will not be considered. However, because this is a public repository, all users are welcome to look a the code for future reference.

## License
[APACHE](https://www.apache.org/licenses/LICENSE-2.0)
