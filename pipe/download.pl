#!/usr/bin/perl
use Net::FTP;
 
 my $host = "ftp.sec.gov";
 my $username = "anonymous";
 my $password = "thecircushaslanded@gmail.com";
  
#-- connect to ftp server
my $ftp = Net::FTP->new($host) or die "Error connecting to $host: $!";
   
#-- login
$ftp->login($username,$password) or die "Login failed: $!";
 
######################### write dir , use "\\" and not "\", for example: "C:\\temp"
$write_dir = "/Users/Robert/Code/Investment";
######################### write dir 

######################### filename with urls (put in same directory as script) 
open dlthis, "8k_to_download.csv" or die $!;
######################### filename with urls (put in same directory as script)

######################### log
open LOG , ">download_log.txt" or die $!;
######################### log

my @file = <dlthis>;

foreach $line (@file) { 
    #CIK, filename, blank is not used (included because it will capture the newline)
    ($CIK, $filename, $blank) = split (",", $line);
    my $ftpdir = "/edgar/data/" . $CIK;
    my $file = $filename;

    # if ( /([0-9|-]+).txt/ ) {
        $filename = $write_dir . "/" . $filename;
        open OUT, ">$filename" or die $!;
        print "file $filename \n";

        #-- chdir to $ftpdir
        # $ftp->cwd($ftpdir) or die "Can't go to $ftpdir: $!";
        $ftp->cwd($ftpdir);
             
        chomp $file;
        #-- download file
        # $ftp->get($file) or die "Can't get $file: $!";
        $ftp->get($file);
        print "file $filename \n";
          

        # my $request = HTTP::Request->new(GET => $get_file);
        # my $response =$ua->get($get_file );
        # $p = $response->content;
        # if ($p) {
        # print OUT $p;
        # close OUT;
        # } else {
        # #error logging
        # print LOG "error in $filename - $CIK \n" ;
        # }
        # }  
}
#-- close ftp connection
$ftp->quit or die "Error closing ftp connection: $!";
close LOG;
