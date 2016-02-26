import re
from glob import glob

filing = """
-----BEGIN PRIVACY-ENHANCED MESSAGE-----
Proc-Type: 2001,MIC-CLEAR
Originator-Name: webmaster@www.sec.gov
Originator-Key-Asymmetric:
 MFgwCgYEVQgBAQICAf8DSgAwRwJAW2sNKK9AVtBzYZmr6aGjlWyK3XmZv3dTINen
 TWSM7vrzLADbmYQaionwg5sDW3P6oaM5D3tdezXMm7z1T+B+twIDAQAB
MIC-Info: RSA-MD5,RSA,
 IKgVogvPwfGNtPuIXUFjD5LvhF3st2L2s/vq0wtgsF5IiELNT7CQOy+q0dJPybhC
 B4nBDqiXOL1JgU/GrW+RNA==

<SEC-DOCUMENT>0000098618-10-000003.txt : 20100115
<SEC-HEADER>0000098618-10-000003.hdr.sgml : 20100115
<ACCEPTANCE-DATETIME>20100115124243
ACCESSION NUMBER:		0000098618-10-000003
CONFORMED SUBMISSION TYPE:	8-K
PUBLIC DOCUMENT COUNT:		1
CONFORMED PERIOD OF REPORT:	20100113
ITEM INFORMATION:		Unregistered Sales of Equity Securities
FILED AS OF DATE:		20100115
DATE AS OF CHANGE:		20100115

FILER:

	COMPANY DATA:	
		COMPANY CONFORMED NAME:			ALANCO TECHNOLOGIES INC
		CENTRAL INDEX KEY:			0000098618
		STANDARD INDUSTRIAL CLASSIFICATION:	COMPUTER STORAGE DEVICES [3572]
		IRS NUMBER:				860220694
		STATE OF INCORPORATION:			AZ
		FISCAL YEAR END:			0610

	FILING VALUES:
		FORM TYPE:		8-K
		SEC ACT:		1934 Act
		SEC FILE NUMBER:	000-09347
		FILM NUMBER:		10529608

	BUSINESS ADDRESS:	
		STREET 1:		15575 N 83RD WAY
		STREET 2:		SUITE 3
		CITY:			SCOTTSDALE
		STATE:			AZ
		ZIP:			85260
		BUSINESS PHONE:		4806071010

	MAIL ADDRESS:	
		STREET 1:		15575 N 83RD WAY
		STREET 2:		SUITE 3
		CITY:			SCOTTSDALE
		STATE:			AZ
		ZIP:			85260

	FORMER COMPANY:	
		FORMER CONFORMED NAME:	ALANCO ENVIRONMENTAL RESOURCES CORP
		DATE OF NAME CHANGE:	19930708

	FORMER COMPANY:	
		FORMER CONFORMED NAME:	ALANCO RESOURCES CORP
		DATE OF NAME CHANGE:	19920703

	FORMER COMPANY:	
		FORMER CONFORMED NAME:	ALANCO LTD
		DATE OF NAME CHANGE:	19901004
</SEC-HEADER>
<DOCUMENT>
<TYPE>8-K
<SEQUENCE>1
<FILENAME>k8011410.txt
<DESCRIPTION>ADDT'L SERIES E OFFERING
<TEXT>
                       SECURITIES AND EXCHANGE COMMISSION
                             WASHINGTON, D.C. 20549


                                    FORM 8-K

                                 CURRENT REPORT

                       Pursuant to Section 13 or 15(d) of
                      The Securities Exchange Act of 1934



                                January 13, 2010
                               ------------------
                                (Date of Report)

                           ALANCO TECHNOLOGIES, INC.
                           -------------------------
             (Exact name of Registrant as specified in its charter)


                                    0-9437
                                   ---------
                             (Commission File No.)

                    ARIZONA                        86-0220694
         ---------------------------     ---------------------------------
        (State of other jurisdiction(    (IRS Employer Identification No.)



             15575 N 83RD WAY, SUITE 3, SCOTTSDALE, ARIZONA  85260
             -------------------------------------------------------
            (Address of Principal Executive Office)       (Zip Code)


                                 (480) 607-1010
              ----------------------------------------------------
              (Registrant's telephone number, including area code)


Check the appropriate box below if the Form 8-K filing is intended to
simultaneously safisfy the filing obligation of the registrant under any of
the following provisions (see General Instruction A.2. below):

(  ) Written communication pursuant to Rule 425 under the Securities Act
     (17 CFR 230.425)

(  ) Soliciting material pursuant to Rule 14a-12 under the Exchange Act
     (17 CFR 240.14a-12)

(  ) Pre-commencement communications pursuant to Rule 14d-2(b) under the
     Exchange Act (17 CFR 240.14d-2(b))

(  ) Pre-commencement communications pursuant to Rule 13e-4(c) under the
     Exchange Act (17 CFR 240.13e-4(c))

Item 3.02  Unregistered Sales of Equity Securities

On January 13, 2010, subsequent to Form 8-K filed on October 28, 2009, the
Company completed an additional private offering of convertible shares of
Series E Preferred Stock.  The proceeds, received by the Company from this
January 13, 2010 offering was $67,500.


                                   SIGNATURE

     Pursuant to the requirements of the Securities Exchange Act of 1934, the
registrant has duly caused this report to be signed on its behalf by the
undersigned hereunto duly authorized.

Date: January 13, 2010                  ALANCO TECHNOLOGIES, INC.

                                        By: /s/John A Carlson
                                            -----------------------
                                            Chief Financial Officer
</TEXT>
</DOCUMENT>
</SEC-DOCUMENT>
-----END PRIVACY-ENHANCED MESSAGE-----"""



def extract_basic_data(txt_file):
    items = []
    with open(txt_file, 'r') as f:
        for s in [r"		COMPANY CONFORMED NAME:*", r"FILED AS OF DATE:*:", r"^ITEM INFORMATION:.*"]:
            items.extend(re.findall(s, f.read(), flags=re.MULTILINE))
    return items


