#!/usr/bin/perl
use strict;

my $buffer = $ENV{'QUERY_STRING'};
my ($baseColor,$channel,$date,$enc) = split(/&/,$buffer);

my $i;
my @nick;
my @colors = ('aqua','yellow','lime','fuchsia','orange','Teal','red','Purple','Maroon','Green');
my $logdir = "/home/2TB/irclog/";
my $script_name = "log_script_w.cgi";
my $cssFile;

if ($baseColor == undef){
    $cssFile = "../../irclog_w.css";
}elsif($baseColor == "w"){
    $cssFile = "../../irclog.css";
}else{
    $cssFile = "../../irclog.csss";
}

print "Content-type: text/html", "\n\n";
print <<EOM;
<html>\n <head>\n
<link rel="stylesheet" type="text/css" href="$cssFile">\n
</head>\n <body>\n<div id="main">
EOM
    print $baseColor;

if ($buffer ==  undef){
    &getfol;
}elsif($date == undef){
    &getfiles;
}else{
    &getlog;
}
print <<EOM;
</div>\n</body>\n</html>\n
EOM

sub getlog{
    chdir($logdir);
    my @follist= glob "*/";
    my $folname = $follist[$channel - 1];
    my $line;
    print "$folname<br>\n";
    chdir("$logdir$folname");
    open(IN, $date);
    while ( $line = <IN>) {
	print &rewrite($line);
	$i++;
    }
    print @nick;
    close(IN);
}

sub getfiles{
    my $req = $channel;
    chdir("$logdir");
    my @follist= glob "*/";
    my $folname = $follist[$req - 1];
    print "$folname<br>\n aa\n";
    chdir("$logdir$folname");
    my @filelist= glob "*.txt";
    foreach my $file (sort @filelist){
	next if( $file =~ /^\.{1,2}$/ );
	&href("$script_name?$baseColor&$channel&$file",$file,"br");
    }
}

sub getfol{
    chdir("$logdir");
    my @file= glob "*/";
    my $i = 1;
    foreach my $direct (@file){
	next if( $direct =~ /^\.{1,2}$/ );
	&href("$script_name?$baseColor&$i",$direct,"br");
	$i = $i + 1;
    }
}

sub href {
    my($url, $alt, $br) = @_;
    print"<a href\=$url>$alt<\/a>";
    if ($br eq "br") {print "<br>";}
    print "\n";
}

sub rewrite{
    my $string = @_[0];
    my $tennpo;
    my $nick_color;

    
    if($string =~ m/^(\d\d:\d\d)\s\W(\S+?:)/){
	$tennpo = $2 . "<br>";
	if (!grep(/$tennpo/,@nick)){
	    push(@nick,$tennpo);
	}
    }
    $nick_color = @colors[(&nick_search($tennpo,@nick) % scalar(@colors))];
    $string =~ s/</\&lt\;/g;
    $string =~ s/^(\d\d:\d\d)\s\W(\S+?:)/<span style="color:blue;">\1<\/span><span style="color:$nick_color ;"> \2<\/span>/;
    if ($string =~ m/.*(http.*?)\s/o){
	$tennpo = $1;
	$string =~ s/(s?https?:\/\/[-_.!~*'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)/<a href=\"$1\" target="_blank" >$1 <\/a>/gi;
	if($tennpo =~ /(jpg)|(png)|(gif)$/){
	    return "<img height=200 src=\"$tennpo \"><br>" . $string . "<br>\n";
	}
	elsif($tennpo =~ /http:\/\/www\.youtube\.com\/.*v=([^&]+).*/){
	    return "<img height=200 src=\"http\:\/\/i.ytimg\.com\/vi\/$1/default.jpg \"><br>" . $string . "<br>\n";
	}else{
	    return "<img src=\"http\:\/\/capture.heartrails.com\/\?$tennpo \"><br>" . $string . "<br>\n";
	}
	return $string ."<br>\n";
    }else{
	return $string . "<br>\n";
    }
}

sub rewrite_time{
    my $time =@_;
}

sub nick_search {
    my $area;
    my ($what, @area) = @_;
    foreach my $idx (0..$area) {
	if ($area[$idx] =~ /$what/) { return $idx }
    }
    return -1;
}
