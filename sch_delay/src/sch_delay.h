#include <linux/pkt_sched.h>
#include <linux/skbuff.h>
#include <linux/kfifo.h>
#include <linux/kdev_t.h>
#include <linux/cdev.h>
#include <linux/rbtree.h>
#include <net/pkt_sched.h>

#define TRUE 1
#define FALSE 0

signed long long get_next_delay(struct kfifo *delay_queue);

/*
    Private data of the qdisc, holds instace-specific information.
*/
struct delay_qdisc_data {
	struct qdisc_watchdog watchdog;

    struct rb_root package_queue_root;

    struct kfifo delay_queue;

    bool reorder_enabled;
    char net_dev_name[50];

    // Chardev
    int chr_dev_majour_num;
    char chr_dev_name[50];
    struct class *dev_class;
    int chr_dev_open_count;


    // Needs to be last element for containe_of!
    struct cdev c_dev; 
};

/*
    Config Structure for communication with "tc".
*/
struct tc_delay_qopt {
	bool	 reorder;
    __u32      limit;
};

/*
    Data inside SKBs.
*/
struct delay_skb_cb {
    signed long long earliest_send;
};



