Email-Format.txt:
	This file contains the markup of the e-mail template (alternate).

	Fields are surrounded by braces. For example: {field_name}.

Email-Format.html:
	This file contains the markup of the e-mail template.

	Fields are surrounded by braces. For example: {field_name}.

Email-Header.txt:
	This file defines the e-mail header information.

	The field name is defined first, followed by a colon &
	a space, followed by the value.	

	Every field and it's corresponding value should use an
	individual line.

	The field name should be lowercase and without spaces.

	The value can contain any character except a colon.

	The value may be also contain another field.

	The fields "To", "From", and "Subject" are required for this file.

	Example entry: "field_name: field value".

Settings.txt:
	This file defines hard values for certain fields.

	The field name is defined first, followed by a colon &
	a space, followed by the value.	

	Every field and it's corresponding value should use an
	individual line.

	The field name should be lowercase and without spaces.

	The value can contain any character except a colon.

	The fields "rti_user", "rti_passwd", "gmail_user", and
	"gmail_passwd" are required for this file.

	Example entry: "field_name: field value".

SendEmail.py:
	The python program itself.

	Usage:
		python SendEmail.py ordernumber img1,img2