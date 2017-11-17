# MALListsMergerPy
Implementation of https://github.com/m4st3rP/MyAnimeListUserListsMerger in python 2.7.

Code was haphazardly written in one sitting and not anywhere near production level. Probably will break if you don't treat it well. For now, just a proof of concept that may or may not be continued.

Usage instructions:
Copy plain text dump from http://affinity.animesos.net/ into first window. Submit will run the program and print back the results in the second window. Export will save the results to a file (MALdump.txt in the current directory). Optionally, a username can also be specified. If one is, all previously seen entries are ignored. Expected input is as follows:

<pre>
#	UserName	Shared	Affinity	Last Online	Birthday	Gender	Joined	Location
1	[ex0]	11	96	Oct 18, 2017	Jun 27, 1997	Female	Oct 13, 2012	Romania, Bucharest
2	[ex1]	13	95	Nov 11, 2017			Feb 3, 2015	Sweden
3	[ex2]	11	95	Oct 21, 2017			Aug 8, 2017	
4	[ex3]	11	94	Oct 30, 2017	Mar 10, 1997	Male	Feb 18, 2015	
5	[ex4]	12	94	Dec 17, 2014			Apr 22, 2013	
etc.
</pre>

Algorithmically, MALListsMergerPy borrows as closely as possible from the original, and should be functionally the same, with the one exception that MALListsMergerPy does not count shows that have not been rated.
