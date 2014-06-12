#!/usr/bin/perl

use Cwd 'abs_path';
use File::Basename;

open (N, dirname(abs_path($0)) . "/word-lists/basic-nouns");
while ($n = <N>) {
	chomp $n;
	push (@n, $n);
}
close (N);

open (V_T, dirname(abs_path($0)) . "/word-lists/basic-verbs-t");
while ($v_t = <V_T>) {
	chomp $v_t;
	push (@v_t, $v_t);
}
close (V_T);

open (V_I, dirname(abs_path($0)) . "/word-lists/basic-verbs-i");
while ($v_i = <V_I>) {
	chomp $v_i;
	push (@v_i, $v_i);
}
close (V_I);

open (ADJ, dirname(abs_path($0)) . "/word-lists/basic-adjectives");
while ($adj = <ADJ>) {
	chomp $adj;
	push (@adj, $adj);
}
close (ADJ);

open (ADV, dirname(abs_path($0)) . "/word-lists/basic-adverbs");
while ($adv = <ADV>) {
	chomp $adv;
	push (@adv, $adv);
}
close (ADV);

open (P, dirname(abs_path($0)) . "/word-lists/basic-prepositions");
while ($p = <P>) {
	chomp $p;
	push (@p, $p);
}
close (P);

open (ART, dirname(abs_path($0)) . "/word-lists/basic-articles");
while ($art = <ART>) {
	chomp $art;
	push (@art, $art);
}
close (ART);

sub my_rand {
	my $range = $_[0] + 1;
	$bits -= log ($range) / log (2);
	return rand ($range);
}

sub noun_phrase {
	print "$art[my_rand($#art)] ";
	if (my_rand (1) < 1) {
		print "$adj[my_rand($#adj)] ";
	}
	print "$n[my_rand($#n)] ";
}

sub sentence {
	noun_phrase();
	if (my_rand (1) < 1) {
		print "$v_i[my_rand($#v_i)] ";
	}
	else {
		print "$v_t[my_rand($#v_t)] ";
		noun_phrase();
	}
	if (my_rand (1) < 1) {
		print "$adv[my_rand($#adv)] ";
	}
	if (my_rand (1) < 1) {
		print "$p[my_rand($#p)] ";
		noun_phrase();
	}
	print "\n";
}

$bits = $ARGV[0];
die "Usage: basic-english <num_bits>\n" unless $bits;
srand();

while ($bits > 0) {
	sentence();
}
