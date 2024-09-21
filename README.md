# Private Key Search and Ultra-Lightweight Database with Public Keys

## Overview

This project implements a database designed to store interleaved bit patterns (010101...) of 15 bits or more in length. These patterns (Pp) are stored along with the number of public keys between patterns (Bi) and the total bits traversed to the end of each pattern (Tb).

**requirements:**

secp256k1

https://github.com/iceland2k14/secp256k1

## Database Structure

The database stores data in the following format:

Bi: 13806, Pp: 010101010101010, Tb: 13821 

Bi: 10889, Pp: 101010101010101, Tb: 24725 

Bi: 10637, Pp: 101010101010101, Tb: 35377 

Bi: 186843, Pp: 010101010101010, Tb: 222235



This format allows the representation of thousands of public keys to be stored in just a few lines, making the database lightweight and easy to manage.

## Search Functionality

To find matches, the search script processes between 10,000 and 250,000 public keys per cycle (low_m). You can configure this value at your discretion; 100,000 is recommended, as it is the average number of keys between patterns.

For example, if there are 50,000 public keys between pattern A and pattern B, starting at an intermediate point between both patterns will easily lead you to the next pattern, and the script will calculate your private key.

## Performance

The speed of the search depends on the size of your database. For instance, if you have a database of 100 million keys and your computer processes 1 million keys per second, you would be processing around 1 billion keys per second.

## Implementation Notes

This project is an implementation of an idea and is not optimized for speed or efficiency. You can create your own implementation in C. 

At the moment, I don't have the computational resources to integrate into the world of GPUs and CPUs in C.

---

**Donate to:**
**btc: bc1qxs47ttydl8tmdv8vtygp7dy76lvayz3r6rdahu**
