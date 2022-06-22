![Banner](https://github.com/erwann-rch/Blitz/blob/main/banner.jpg)

# /!\ WORK IN PROGRESS ...

# Blitz

A Python-based chess program containing a local multiplayer system, an AI-versus mode, accurate moves and many other features.

[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)  [![forthebadge](http://forthebadge.com/images/badges/powered-by-electricity.svg)](http://forthebadge.com)

## Table of Contents

1. [General Info](#general-info)
2. [TODO-LIST](#todo-list)
3. [Technologies](#technologies)
4. [Installation](#installation)
5. [Licence](#licence)

### General Info
***
This program is a python project that I made in order to prove what I can do in terms of programming.
Moreover, I enjoyed merging two of my passions: chess and programming. Hope you will find it at your taste.

## TODO-LIST 
***

* Required
- [x] Drawn board / pieces / allow piece move (anywhere)
- [x] Turns
- [x] Make / Undo move
- [x] All possible moves
- [x] Checkmate / Stalemate
- [x] Legal moves
- [x] Special rules in chess (castling / en-passant / pawn promotion)
- [x] 3 identical moves = stalemate
- [x] Only kings left = stalemate
- [x] Add proper chess notation
- [x] Highlight of selected squares / allowed moves / last opponent move
- [x] AI

* Unrequired
- [ ] Highlight circles and not square
- [ ] Drag N Drop 
- [ ] Add a clock
- [x] Add choice for the pawn promotion
- [ ] Add prettier end game text
- [ ] Menu of preferences :
  - [ ] Select theme (brown/blue/green/gray[default])
  - [ ] Select which mode (AI VS Human[default] / Human VS Human)
    - [ ] If AI mode selected => choose what side to play (white[deault] / black / random)
  - [ ] Select if highlight moves[default] or not
- [ ] Local multiplayer 
- [ ] Flip the board on each turn (only if mutliplayer)
- [ ] Generate .pgn file

## Technologies
***
A list of technologies used within the project:
* [Python 3.X](https://www.python.org) 
* [Pygame](https://www.pygame.org/docs/)

## Installation
***
A little help about the installation. 
```
$ pip install pygame
$ git clone https://github.com/erwann-rch/Blitz/
$ cd ../Blitz/codes
$ python3 Main.py
```

## Usage
***
- Hit ```U``` to ```undo``` a move
- Hit ```Esc``` to ```reset``` the game

### Licence

This projet is under ```GPU General Public License v3.0```
