emcc --bind -s ALLOW_MEMORY_GROWTH=1 -O3 -std=c++14 -I. -I/opt/boost/include ./module.cpp ./seir.cpp -o ./seirmodel5.js 
