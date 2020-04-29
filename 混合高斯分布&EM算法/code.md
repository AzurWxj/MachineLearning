# Hash

```java
static final int hash(Object key) {
    int h;
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}
```

```java
public V put(K key, V value) {
    return putVal(hash(key), key, value, false, true);
}
```

```java
/*
 * @param onlyIfAbsent if true, don't change existing value
 * @param evict if false, the table is in creation mode.
 * @return previous value, or null if none
*/
final V putVal(int hash, K key, V value, boolean onlyIfAbsent,
                   boolean evict) {
    Node<K,V>[] tab; Node<K,V> p; int n, i;
    if ((tab = table) == null || (n = tab.length) == 0)
        n = (tab = resize()).length;
    if ((p = tab[i = (n - 1) & hash]) == null)
        tab[i] = newNode(hash, key, value, null);
    else {
        Node<K,V> e; K k;
        if (p.hash == hash &&
            ((k = p.key) == key || (key != null && key.equals(k))))
            e = p;
        else if (p instanceof TreeNode)
            e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);
        else {
            for (int binCount = 0; ; ++binCount) {
                if ((e = p.next) == null) {
                    p.next = newNode(hash, key, value, null);
                    if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st
                        treeifyBin(tab, hash);
                    break;
                }
                if (e.hash == hash &&
                    ((k = e.key) == key || (key != null && key.equals(k))))
                    break;
                p = e;
            }
        }
        if (e != null) { // existing mapping for key
            V oldValue = e.value;
            if (!onlyIfAbsent || oldValue == null)
                e.value = value;
            afterNodeAccess(e);
            return oldValue;
        }
    }
    ++modCount;
    if (++size > threshold)
        resize();
    afterNodeInsertion(evict);
    return null;
}
```

# ARP报文格式
<table>
<tr><td colspan="2">硬件类型</td><td>协议类型</td></tr>
<tr><td>硬件地址长度</td><td>协议长度</td><td>操作类型</td></tr>
<tr><td colspan="3">发送方硬件地址（0-3字节）</td></tr>
<tr><td colspan="2">发送方硬件地址（4-5字节）</td><td>发送方IP地址（0-1字节）</td></tr>
<tr><td colspan="2">发送方IP地址（2-3字节）</td><td>目标硬件地址（0-1字节）</td></tr>
<tr><td colspan="3">目标硬件地址（2-5字节）</td></tr>
<tr><td colspan="3">目标IP地址（0-3字节）</td></tr>
</table>


# 一些问题

1. private修饰的方法可以通过反射访问，那么private的意义是什么
    >java的private修饰符并不是为了绝对安全性设计的，更多是对用户常规使用java的一种约束；2.从外部对对象进行常规调用时，能够看到清晰的类结构。
2. Java类初始化顺序
   >基类静态代码块，基类静态成员字段（并列优先级，按照代码中出现的先后顺序执行，且只有第一次加载时执行）——>派生类静态代码块，派生类静态成员字段（并列优先级，按照代码中出现的先后顺序执行，且只有第一次加载时执行）——>基类普通代码块，基类普通成员字段（并列优点级，按代码中出现先后顺序执行）——>基类构造函数——>派生类普通代码块，派生类普通成员字段（并列优点级，按代码中出现先后顺序执行）——>派生类构造函数
3. 对方法区和永久区的理解以及它们之间的关系
   >方法区是jvm规范里要求的，永久区是Hotspot虚拟机对方法区的具体实现，前者是规范，后者是实现方式。jdk1.8作了改变。
4. 一个java文件有3个类，编译后有几个class文件
   1. >文件中有几个类编译后就有几个class文件。
5. 局部变量使用前需要显式地赋值，否则编译通过不了，为什么这么设计
   1. >成员变量是可以不经初始化的，在类加载过程的准备阶段即可给它赋予默认值，但局部变量使用前需要显式赋予初始值，javac不是推断不出不可以这样做，而是没有这样做，对于成员变量而言，其赋值和取值访问的先后顺序具有不确定性，对于成员变量可以在一个方法调用前赋值，也可以在方法调用后进行，这是运行时发生的，编译器确定不了，交给jvm去做比较合适。而对于局部变量而言，其赋值和取值访问顺序是确定的。这样设计是一种约束，尽最大程度减少使用者犯错的可能（假使局部变量可以使用默认值，可能总会无意间忘记赋值，进而导致不可预期的情况出现）。
6. ReadWriteLock读写之间互斥吗
   1. >ReadWriteRock 读写锁，使用场景可分为读/读、读/写、写/写，除了读和读之间是共享的，其它都是互斥的，接着会讨论下怎样实现互斥锁和同步锁的， 想了解对方对AQS，CAS的掌握程度，技术学习的深度。
7. Semaphore拿到执行权的线程之间是否互斥
   1. >Semaphore拿到执行权的线程之间是否互斥，Semaphore、CountDownLatch、CyclicBarrier、Exchanger 为java并发编程的4个辅助类，面试中常问的 CountDownLatch CyclicBarrier之间的区别，面试者肯定是经常碰到的， 所以问起来意义不大，Semaphore问的相对少一些，有些知识点如果没有使用过还是会忽略，Semaphore可有多把锁，可允许多个线程同时拥有执行权，这些有执行权的线程如并发访问同一对象，会产生线程安全问题。
8. 写一个你认为最好的单例模式
9.  B树和B+树是解决什么样的问题的，怎样演化过来，之间区别
    1.  >B树和B+树，这题既问mysql索引的实现原理，也问数据结构基础，首先从二叉树说起，因为会产生退化现象，提出了平衡二叉树，再提出怎样让每一层放的节点多一些来减少遍历高度，引申出m叉树，m叉搜索树同样会有退化现象，引出m叉平衡树，也就是B树，这时候每个节点既放了key也放了value，怎样使每个节点放尽可能多的key值，以减少遍历高度呢（访问磁盘次数），可以将每个节点只放key值，将value值放在叶子结点，在叶子结点的value值增加指向相邻节点指针，这就是优化后的B+树。然后谈谈数据库索引失效的情况，为什么给离散度低的字段（如性别）建立索引是不可取的，查询数据反而更慢，如果将离散度高的字段和性别建立联合索引会怎样，有什么需要注意的？
10. 写一个生产者消费者模式
    1.  >生产者消费者模式，synchronized锁住一个LinkedList，一个生产者，只要队列不满，生产后往里放，一个消费者只要队列不空，向外取，两者通过wait()和notify()进行协调，写好了会问怎样提高效率，最后会聊一聊消息队列设计精要思想及其使用。
11. 写一个死锁
    1.  死锁产生的原因
        1.  系统资源的竞争，系统资源的竞争导致系统资源不足，以及资源分配不当，导致死锁。
        2.  进程运行推进顺序不合适，进程在运行过程中，请求和释放资源的顺序不当，会导致死锁。
    2.  死锁的四个必要条件
        1. 互斥条件：一个资源每次只能被一个进程使用，即在一段时间内某 资源仅为一个进程所占有。此时若有其他进程请求该资源，则请求进程只能等待。
        2. 请求与保持条件：进程已经保持了至少一个资源，但又提出了新的资源请求，而该资源 已被其他进程占有，此时请求进程被阻塞，但对自己已获得的资源保持不放。
        3. 不可剥夺条件：进程所获得的资源在未使用完毕之前，不能被其他进程强行夺走，即只能 由获得该资源的进程自己来释放（只能是主动释放)。
        4. 循环等待条件：若干进程间形成首尾相接循环等待资源的关系
     1. 写一个死锁
        1. >定义两个ArrayList,将他们都加上锁A,B，线程1,2，1拿住了锁A ，请求锁B，2拿住了锁B请求锁A，在等待对方释放锁的过程中谁也不让出已获得的锁。
        2. ```java
            public class DeadLock {
                public static void main(String[] args) {
                    final List<Integer> list1 = Arrays.asList(1, 2, 3);
                    final List<Integer> list2 = Arrays.asList(4, 5, 6);
                    new Thread(new Runnable() {
                        @Override
                        public void run() {
                            synchronized (list1) {
                                for (Integer i : list1) {
                                    System.out.println(i);
                                }
                                try {
                                    Thread.sleep(1000);
                                } catch (InterruptedException e) {
                                    e.printStackTrace();
                                }
                                synchronized (list2) {
                                    for (Integer i : list2) {
                                        System.out.println(i);
                                    }
                                }
                            }
                        }
                    }).start();

                    new Thread(new Runnable() {
                        @Override
                        public void run() {
                            synchronized (list2) {
                                for (Integer i : list2) {
                                    System.out.println(i);
                                }
                                try {
                                    Thread.sleep(1000);
                                } catch (InterruptedException e) {
                                    e.printStackTrace();
                                }
                                synchronized (list1) {
                                    for (Integer i : list1) {
                                        System.out.println(i);
                                    }
                                }
                            }
                        }
                    }).start();

                }
            }
            ```
12. cpu 100%怎样定位
13. String a = "ab"; String b = "a" + "b"; a == b 是否相等，为什么
    1.  >String a = "ab"; String b = "a" + "b"; a ，b 是相等的
14. int a = 1; 是原子性操作吗
    1.  >int a = 1; 是原子性操作。
15. 可以用for循环直接删除ArrayList的特定元素吗？可能会出现什么问题？怎样解决
    1.  >for循环直接删除ArrayList中的特定元素是错的，不同的for循环会发生不同的错误，泛型for会抛出 ConcurrentModificationException，普通的for想要删除集合中重复且连续的元素，只能删除第一个。
    2.  >打开JDK的ArrayList源码，看下ArrayList中的remove方法（注意ArrayList中的remove有两个同名方法，只是入参不同，这里看的是入参为Object的remove方法）是怎么实现的，一般情况下程序的执行路径会走到else路径下最终调用fastRemove方法,会执行System.arraycopy方法，导致删除元素时涉及到数组元素的移动。
        >
        >针对普通for循环的错误写法，在遍历第一个字符串b时因为符合删除条件，所以将该元素从数组中删除，并且将后一个元素移动（也就是第二个字符串b）至当前位置，导致下一次循环遍历时后一个字符串b并没有遍历到，所以无法删除。针对这种情况可以倒序删除的方式来避免
    3. >解决方案：用 Iterator。
        ```java
        List<String> list = new  ArrayList(Arrays.asList("a", "b",  "b" , "c", "d"));
        Iterator<String> iterator = list.iterator();
        while(iterator.hasNext()) {
            String element = iterator.next();
            if(element.equals("b")) {
                iterator.remove();
            }
        }
        ```
        iterator的遍历中会维护一个游标cursor，用来记录下一个要遍历的元素的下标，当使用iterator的remove时他会删除当前元素，但是它会保持游标cursor不变，不会自增1，因为ArrayList删除元素后会把后面的元素全部向前挪一位，所以下一个元素的下标就是当前删除的元素的下标，所以保持游标不变
1.  新的任务提交到线程池，线程池是怎样处理
    1.  程池判断核心线程池里的线程是否都在执行任务。如果不是，则创建一个新的工作线程来执行任务。如果核心线程池里的线程都在执行任务，则执行第二步。
    2.  线程池判断工作队列是否已经满。如果工作队列没有满，则将新提交的任务存储在这个工作队列里进行等待。如果工作队列满了，则执行第三步。
    3.  线程池判断线程池的线程是否都处于工作状态。如果没有，则创建一个新的工作线程来执行任务。如果已经满了，则交给饱和策略来处理这个任务。
2.  AQS和CAS原理
    1.  **抽象队列同步器AQS**（AbstractQueuedSychronizer），如果说java.util.concurrent的基础是CAS的话，那么AQS就是整个Java并发包的核心了，ReentrantLock、CountDownLatch、Semaphore等都用到了它。AQS实际上以双向队列的形式连接所有的Entry，比方说ReentrantLock，所有等待的线程都被放在一个Entry中并连成双向队列，前面一个线程使用ReentrantLock好了，则双向队列实际上的第一个Entry开始运行。AQS定义了对双向队列所有的操作，而只开放了tryLock和tryRelease方法给开发者使用，开发者可以根据自己的实现重写tryLock和tryRelease方法，以实现自己的并发功能。
    2. **比较并替换CAS**(Compare and Swap)，假设有三个操作数：内存值V、旧的预期值A、要修改的值B，当且仅当预期值A和内存值V相同时，才会将内存值修改为B并返回true，否则什么都不做并返回false，整个比较并替换的操作是一个原子操作。CAS一定要volatile变量配合，这样才能保证每次拿到的变量是主内存中最新的相应值，否则旧的预期值A对某条线程来说，永远是一个不会变的值A，只要某次CAS操作失败，下面永远都不可能成功。
    3.  CAS虽然比较高效的解决了原子操作问题，但仍存在三大问题。
        1.  循环时间长开销很大。
        2.  只能保证一个共享变量的原子操作。
        3.  ABA问题。
3.  synchronized底层实现原理
4.  volatile作用，指令重排相关
    1.  多线程主要围绕可见性和原子性两个特性而展开，使用volatile关键字修饰的变量，保证了其在多线程之间的可见性，即每次读取到volatile变量，一定是最新的数据
    2.  代码底层执行不像我们看到的高级语言—-Java程序这么简单，它的执行是Java代码–>字节码–>根据字节码执行对应的C/C++代码–>C/C++代码被编译成汇编语言–>和硬件电路交互，现实中，为了获取更好的性能JVM可能会对指令进行重排序，多线程下可能会出现一些意想不到的问题。使用volatile则会对禁止语义重排序，当然这也一定程度上降低了代码执行效率
5.  AOP和IOC原理
    1.  >AOP可以看做是对OOP的补充，对代码进行横向的扩展，通过代理模式实现，代理模式有静态代理，动态代理，Spring利用的是动态代理，在程序运行过程中将增强代码织入原代码中。IOC是控制反转，将对象的控制权交给Spring框架，用户需要使用对象无需创建，直接使用即可。AOP和IOC最可贵的是它们的思想。
6.  Spring怎样解决循环依赖的问题
7.  dispatchServlet怎样分发任务的
8.  mysql给离散度低的字段建立索引会出现什么问题，具体说下原因


# 集合

## HashMap

* [阿里一面，和面试官扯了半小时的HashMap](https://zhuanlan.zhihu.com/p/130437181)
* [HashMap几个刁钻的面试题，第六个我就跪了](https://zhuanlan.zhihu.com/p/87929020)
* [HashMap？ConcurrentHashMap？相信看完这篇没人能难住你！](https://blog.csdn.net/weixin_44460333/article/details/86770169)
* [ConcurrentHashMap的实现原理和源码分析](https://blog.csdn.net/weixin_28760063/article/details/81211988)
* [ConcurrentHashMap底层实现原理(JDK1.7 & 1.8)](https://www.jianshu.com/p/865c813f2726)

# 多线程

## 可重入锁

* [Java可重入锁详解](https://www.jianshu.com/p/f47250702ee7)
