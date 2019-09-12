# chaos engineering

### 

As an industry, we are quick to adopt practices that increase the flexibility of developement and velocity of deployment. But how much confidence do we have on the complex systems we put out in production. Chaos engineering is the discipline of experimenting on a distributed system oin oder to gain confidence in a system's capability to withstand turbulent conditions in production. To address this uncertainty, we will be running a set of experiments to uncover systemic weaknesses.

In this experiment, we will be deploying two instances of a distributed system, a control group and an experimental group. We also will definte a 'steady state' which will indicate some sort of normal behavior for the distributed system.

We will deploy each distributed system using AWS EKS. 
A distributed system will consist of ...TODO
The steady state criteria will be...TODO

We will be running a set of tests on the experimental group which will try to disrupt the steady state, giving us more confidence in our system.

Tests:

  - Will the system will be able to handle CPU / shutdown attacks at the container level using [Gremlin Free](https://www.gremlin.com/docs/)
  - Will the system be able to handle attacks at the pod level?

Results:

  - need to figure out how we test steady state, what metrics from the distributed system are we going to track?
  - for mvp, simplest monitoring mechanism would be CloudWatch?

### References

 - [Principles of Chaos Engineering](http://principlesofchaos.org/?lang=ENcontent)
 - [awesome-chaos-engineering](https://github.com/dastergon/awesome-chaos-engineering)