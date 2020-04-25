emcc --bind -s ALLOW_MEMORY_GROWTH=1 -O3 -std=c++11 -I. -I/opt/boost/include ./module.cpp ./seir.cpp -o ./seirmodel3.js
