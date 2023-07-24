<div align="center">
<img src=imgs/logo.png width=200>

# K6 UI Runner

</div>
This is a GUI application built with Python and Tkinter for running load tests using k6. It allows the user to input the URL of the application to be tested, set multiple durations, and the number of targets for each duration. The stages are flexible and dynamically generated based on user input. The output of the load test is displayed in real-time within the application.

## Requirements

The following are required to run the application:

1. Python 3.7 or above: You can download it from [Python's official site](https://www.python.org/).
2. pip: It comes pre-installed with Python 3.4 and above. If for some reason, it's not installed, you can refer to [pip's official installation guide](https://pip.pypa.io/en/stable/installing/).
3. Tkinter: It is included in the Python standard library.
4. k6: This is used for load testing. You can download it from [k6's official site](https://k6.io/).

## Running the Application

1. Clone this repository to your local machine.
2. Open a terminal/command prompt.
3. Navigate to the directory where the repository is cloned.
4. Run the following command to start the application.

```
./k6-ui-runner
```

5. The application window should open, and you can now use the application.

<div align="center">
<img src=imgs/app.png width=600>
</div>

6. Add the URL of your application that you would like to apply the load test on in the URL field.

7. Write the number of durations you would like to apply then `Generate Fields` then add how long each duration should be and how many targets to apply in each duration as shown in the image.

<div align="center">
<img src=imgs/generate.png width=600>
</div>

Here we are having `3` times to run load-test the first duration is `4 Seconds` will apply `50 targets` then `10 Seconds` with `20 targets` and finally for `30 Seconds` with `100 target`.

8. When you click `RUN` you should be able to see the results in the output area as shown below.

<div align="center">
<img src=imgs/run.png width=600>
</div>

### `NOTE:` That will generate `test.js` file in the current directory with the your inputs.

```
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    stages: [
    { duration: '4s', target: 50 },{ duration: '10s', target: 20 },{ duration: '30s', target: 100 }
    ],
};

export default function () {
    const res = http.get('http://test.k6.io');
    check(res, { 'status was 200': (r) => r.status == 200 });
    sleep(1);
}
```
