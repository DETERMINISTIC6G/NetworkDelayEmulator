/* SPDX-License-Identifier: GPL-2.0-or-later */
/*
 * q_delay.c		Delay.
 *
 * Authors:	Lorenz Grohmann, <st161568@stud.uni-stuttgart.de>
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>

#include "utils.h"
#include "tc_util.h"


struct tc_delay_qopt {
	bool	 reorder;
	__u32		 limit;
};

static void explain(void)
{
	fprintf(stderr, "Usage: tc qdisc { add | replace | change } ... delay limit <BYTES> reorder <True/False>\n\n");
}

static int delay_parse_opt(struct qdisc_util *qu, int argc, char **argv,
			  struct nlmsghdr *n, const char *dev)
{
	int ok = 0;
	struct tc_delay_qopt opt = {};

	while (argc > 0) {

		if (strcmp(*argv, "limit") == 0) {
			NEXT_ARG();
			if (get_size(&opt.limit, *argv)) {
				fprintf(stderr, "%s: Illegal value for \"limit\": \"%s\"\n", qu->id, *argv);
				return -1;
			}
			ok++;
		}
		else if (strcmp(*argv, "reorder") == 0) {
			NEXT_ARG();
			if(strcmp(*argv, "True") == 0 || strcmp(*argv, "true") == 0) {
				opt.reorder = true;
			} else if(strcmp(*argv, "False") == 0 || strcmp(*argv, "false") == 0) {
				opt.reorder = false;
			} else {
				fprintf(stderr, "%s: Illegal value for \"reorder\": \"%s\"\n", qu->id, *argv);
				return -1;
			}
			ok++;
		} else if (strcmp(*argv, "help") == 0) {
			explain();
			return -1;
		} else {
			fprintf(stderr, "%s: unknown parameter \"%s\"\n", qu->id, *argv);
			explain();
			return -1;
		}
		argc--; argv++;
	}

	if (ok) {
		addattr_l(n, 1024, TCA_OPTIONS, &opt, sizeof(opt));
	}
	return 0;
}

static int delay_print_opt(struct qdisc_util *qu, FILE *f, struct rtattr *opt)
{
//	struct tc_delay_qopt *qopt;
//	if (opt == NULL)
//		return 0;

	return 0;
}


struct qdisc_util delay_qdisc_util = {
	.id = "delay",
	.parse_qopt = delay_parse_opt,
	.print_qopt = delay_print_opt,
};
