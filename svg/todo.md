# Todo

- fix line length possible overflow
  - because is isn't supported by default in svg, use some js tspan manual solution
- fix loading time
  - if the whole svg is loaded dynamically instead of only the github api fetch content, it might either stop loading anything, or actually work
- change path to use /index.svg rather than /svg/index.svg
  - maybe also change name of index.svg
