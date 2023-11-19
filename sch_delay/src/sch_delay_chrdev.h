#include <linux/init.h>
#include <linux/types.h>
#include <linux/kernel.h>
#include <linux/skbuff.h>
#include <linux/fs.h>
#include <linux/device.h>
#include <linux/kdev_t.h>
#include <linux/err.h>
#include <linux/cdev.h>
#include <linux/kfifo.h>
#include <linux/delay.h>
#include <linux/ktime.h>
#include <linux/string.h>


ssize_t sch_delay_device_read(struct file *file, char *buffer, size_t len, loff_t *offset);

ssize_t sch_delay_device_write(struct file *file, const char *buffer, size_t len, loff_t *offset);

int sch_delay_device_open(struct inode *inode, struct file *file);

int sch_delay_device_release(struct inode *inode, struct file *file);




