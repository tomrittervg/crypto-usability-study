
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <openssl/sha.h>

// RFC 4648
char* alphabet =   "abcdefghijklmnopqrstuvwxyz234567";

#define NUM_CHARS_PER_KEYNAME 25

// Encode 'in' as 125-bit lowercase RFC 4648 base32 into 'out'
void base32_bin2chr2(uint8_t* out, uint8_t* in)
{
	// Handle 40 bits per loop, 3 loops, then finish the last 5 bits
	for (int count=0; count < 3; count++) {		
		out[0] = alphabet[ in[0] >> 3 ]; 
		out[1] = alphabet[ ((in[0] << 2) | (in[1] >> 6)) & 0x1F ]; 
		out[2] = alphabet[ (in[1] >> 1) & 0x1F ]; 
		out[3] = alphabet[ ((in[1] << 4) | (in[2] >> 4)) & 0x1F ]; 
		out[4] = alphabet[ ((in[2] << 1) | (in[3] >> 7)) & 0x1F ]; 
		out[5] = alphabet[ (in[3] >> 2) & 0x1F ]; 
		out[6] = alphabet[ ((in[3] << 3) | (in[4] >> 5)) & 0x1F ]; 
		out[7] = alphabet[ in[4] & 0x1F ];
		out += 8;
		in += 5;
	}
	out[0] = alphabet[ in[0] >> 3 ]; 
}

int score_chunk(uint8_t* in, uint8_t num_bytes) 
{
	uint8_t count = 0;
	uint8_t score = 0;
	uint8_t state = 0; // 1 = prev consonant, 2 = prev vowel
	for (count = 0; count < num_bytes; count++) {
		uint8_t c = *in++;
		if (c >= '2' && c <= '7')
			state = 0;
		else if (c == 'a' || c == 'e'  || c == 'i' || c == 'o' || c == 'u') {
			if (state == 1)
				score++;
			state = 2;
		}
		else {
			if (state == 2)
				score++;
			state = 1;
		}
	}
	return score;
}

int calc_score(uint8_t* in)
{
	uint8_t score = 0;
	score += score_chunk(in, 6);
	score += score_chunk(in+6, 4);
	score += score_chunk(in+10, 5);
	score += score_chunk(in+15, 4);
	score += score_chunk(in+19, 6);
	return score;
}

void format_keyname(char* s, uint8_t* in)
{
	memcpy(s, in, 6);
	s += 6;
	in += 6;
	memcpy(s, " - ", 3);
	s += 3;

	memcpy(s, in, 4);
	s += 4;
	in += 4;
	memcpy(s, " - ", 3);
	s += 3;

	memcpy(s, in, 5);
	s += 5;
	in += 5;
	memcpy(s, " - ", 3);
	s += 3;

	memcpy(s, in, 4);
	s += 4;
	in += 4;
	memcpy(s, " - ", 3);
	s += 3;

	memcpy(s, in, 6);
	s += 6;
	in += 6;
	*s = 0;
}

void u32top(uint8_t* p, uint32_t v)
{
    *p++ = (v >> 24) & 0xFF;
    *p++ = (v >> 16) & 0xFF;
    *p++ = (v >> 8) & 0xFF;
    *p =   (v) & 0xFF;    
}

// Tries hashing the key_to_be_hashed with 32-bit values appended until discovering
// a value which either meets the target_score, or the maximum number of iterations
// is reached.  Leaves the highest-scoring value appended to key-to-be-hashed.
void search_keyname(uint8_t* key_to_be_hashed,
					uint8_t key_len, uint32_t max_iter, uint8_t target_score,
					char* keyname, uint8_t* best_score, uint32_t* best_count)
{
	uint8_t digest[32];
	uint8_t chars[NUM_CHARS_PER_KEYNAME];
	uint32_t count = 0;
	uint8_t score = 0;
	*best_score = 0;
	*best_count = 0;
	for (count = 0; count < max_iter; count++) {
		u32top(key_to_be_hashed + key_len, count);
		SHA256(key_to_be_hashed, key_len + 4, digest);
		base32_bin2chr2(chars, digest);
		score = calc_score(chars);
		if (score > *best_score) {
			*best_score = score;
			*best_count = count+1;
			format_keyname(keyname, chars);
			printf("best_score = %2d, iters = %10u   %s\n", *best_score, *best_count , keyname);
		}
		if (score >= target_score)
			break;
	}
}

int main(int argc, char* argv[])
{
	if (argc < 4) {
		printf("keyname <32-byte key string> <max_iter> <target_score>\n");
		exit(-1);
	}
	uint8_t key_to_be_hashed[36]; // Assume 32-byte key, 4-bytes for nonce
	char keyname[100];
	uint8_t score = 0;
	uint32_t iters = 0;
	uint32_t max_iter = 0;
	uint8_t target_score = 0;

	memcpy(key_to_be_hashed, argv[1], 32);
	max_iter = atoi(argv[2]);
	target_score = atoi(argv[3]);

	search_keyname(key_to_be_hashed, 32, max_iter, target_score, keyname, &score, &iters);
	printf("\n%s\n%d\n%d\n", keyname, score, iters);
	return 0;
}
