"""
reference :  https://github.com/deehzee/unionfind
"""

# 2to3
from __future__ import (
    absolute_import, division, print_function, unicode_literals,
)

# libraries
import numpy as np
import tqdm


class JStree(object):
    """JStree data structure

    JStree is a data sturcture to make joint tree or split tree by image.

    but this class has no attribute for image but image index list index.

    *** image index ***
       if image size is (N,M)  a location of image (i,j) has image index
          image index = i + N*j.
    in this process for positive integes N,M we can obtains image index
       0 , 1, 2, ... , NM -1 and we call this list (image) Index list.

    ** I will omit "image" for convenient writing comment.

    To make joint(split) tree , sorting (image) index list is required.

    making tree works if and only if sorted index list has this property

     * set of index list = { x (which is integer )| 0<=x < N*M }
      # N ,M  essential argument (int) for initializing this object.

    * The length of index list must be N*M. ( No duplication )

    Because of  above conditions JStree.make() spawn tree. ( no cyclic and connected graph)

    All edge in JStree has following property
     The two node of a edge is adjacent.

    In this->make() ,This object make JStree bottom(leaf nodes) to Top(root).
    So in this progress ,  JStree is not one of tree(but forest).

    JStree has JSUFD (Joint Split union find data structure).
    JSUFD is union find data structure always be Forest(all of components are trees).
    since forest consists of disjoint union of trees we use following terms and attributes

    Terms
    -------
    N , M : initializer for JStree (
     N,M must be positive integer finally JStree consists of { 0,1,2,...,NM-1}

    Elements
     indices belonging to JSUFD.(also in Sorted (image)Index list)
    Component
     Elements belonging to the same disjoint tree.

    Connected
        Two elements are connected if they belong to the same component.

    FindRoot
        The operation to find the root of a disjoint tree.

    Adjacent
        Tuple of two elements  (i,j) is adjacent (in JSUFD).
         if (max( absolute(i%N - j%M) , absolute(int(i/M)-int(j/M))) <= 1)

    ProperAdjacent
        if (i,j) is adjacent and i != j , (i , J) is ProperAdjacent

    ProperAdjacent component
     def>> disjoint component A is  ProperAdjacent to B.
        if there exists a in A and b in B such that (a,b) is ProperAdjacent.


    FindAdj
        The operation to find list of root of disticnt ProperAdjacent "components"

    Bifurcation
        The element is Bifurcation if The element is parents two(or more) elements.



    Attributes
    -----------
    n_elts : int
        Number of elements.

    n_comps : int
        Number of disjoint components.

    Implements
    -----------
    __len__
        calling "len(js)" (where "js" is an instance of "JStree")
        returns the number of elements.(number of indices in JSUFD)


    __contains__
        For "js" and instance of "JStree" and x an index :: integer( x in [0,NM) ),
        " x in js" returns "True" if "x" is an element in "js"

    """

    def __init__(self, number_of_img_rows, number_of_img_cols):
        self.N = number_of_img_rows
        self.M = number_of_img_cols

        # information of this instacne
        self.bifurcation_elements = np.zeros(self.N * self.M, dtype=bool)
        """ image indices of bifurcation point 
           self.bifurcation_elements[image_index] is true 
        if and only if 
            image_index is bifurcation element in joint(split) tree.

            this is correct if make function is finished.   
       """
        self.leaf_elements = np.zeros(self.N * self.M, dtype=bool)  # for testing bfalg.

        # private member
        self._made = False  # this is not jstree yet you need to make() .
        self._none = self.N * self.M
        """none is regarded as none type value... for no dynamic allocation.
        because of conditions of sorted index list, "NM" cannot be element.
       """

        self.n_elts = 0  # current number of elements
        self.n_comps = 0  # the number of disjoint trees
        self._n_leaf = 0  # the number of all leaf node over forest
        self._next = 0  # next available index in sorted index list.
        self._is_root = np.zeros(self.N * self.M, dtype=bool)  # It is root element?

        # for speeding up root found function
        self._par_compressed_JSUFD = np.ones(self.N * self.M, dtype=int)  # [1,...,1]
        self._par_compressed_JSUFD = self._par_compressed_JSUFD * self._none  # [_none, ... ,_none]

        #  for the internal tree structure
        self._par = np.ones(self.N * self.M, dtype=int)  # [ 1,...,1]
        self._par = self._par * self._none  # [_none, ... ,_none]

    # public method
    def make(self, array):
        """
        :param array:
        initialize or resetting this structure
        **  let js is instance of "JStree".
            js.make(array) # first
            js.make(array1) # second
            # js lost information about array ,and the first version internal tree was deleted.
            # only information made by  last make function remains.
        * array will be one of member of this . if it changed, the member of this instance changed
            js.make(array1) # second
            modify(array1)# it changes one of member of js
          but , return value of get_functions(getter) Never changed.
        :return: none
        """
        self.sorted_index_list = array  # required input for make()
        # check condition for sorted index list
        cond1 = (self.N * self.M == len(self.sorted_index_list))
        cond2 = set(array) == set([i for i in range(self.N * self.M)])
        if not (cond1 and cond2):
            raise ValueError("you must input {}size array but Its size was {} or not distinct ".format(
                self.N * self.M, len(array)))
        if self._made:
            self.__init__(self.N, self.M)


        for i in tqdm.tqdm(range(self.N * self.M)):
            self.bfalg_add()

        self._made = True

    # get functions ( getter)
    def get_bifurcation_point(self):
        if not self._made:
            raise NotImplementedError("jstree.make( arraytype ) is requreid")
        return np.copy(self.bifurcation_elements)

    def get_leaf_information(self):
        if not self._made:
            raise NotImplementedError("jstree.make( arraytype ) is requreid")
        return np.copy(self.leaf_elements)

    def get_JStree_data(self):
        if not self._made:
            raise NotImplementedError("jstree.make( arraytype ) is requreid")
        return np.copy(self._par)

        # private method

    def _is_illegal(self, element):  # index condition checking
        """
        in this data structure , only non negative integer that below N*M can be element.
        :param element:
        :return: True if "element" can not be element of JStree else return False
        """
        if (self.N * self.M) > element >= 0:
            return False
        else:
            return True  # out of range

    def __len__(self):
        return self.n_elts

    def __contains__(self, item):  # iff item is element
        if self._is_illegal(item):  # The item can not be element
            return False
        if self._par[item] == self._none:  # The item is not element
            return False
        return True

    def _definitely_contains(self, item):
        if not self.__contains__(item):
            return False
        if self._par_compressed_JSUFD[item] == item and self._par[item] == item:
            return True
        root = self._find_root(item)
        return self._definitely_contains(root)

    def _find_root(self, x):
        """Find the root of the disjoint set containing the given element.
        Parameters
        ----------
        x : immutable object
        Returns
        -------
        int
            The (index of the) root.
        Raises
        ------
        ValueError
            If the given element is not found.
        """
        if self._is_illegal(x):
            raise ValueError('{} is illegal element'.format(x))

        if x not in self:
            return self._none
        if self._is_root[x]:
            return x

        p = x

        while p != self._par_compressed_JSUFD[p]:

            # path compression
            q = self._par_compressed_JSUFD[p]
            self._par_compressed_JSUFD[p] = self._par_compressed_JSUFD[q]

            if self._is_illegal(q):
                raise ValueError('element {} has wrong parent {}'.format(p, q))
            if q == self._none:
                raise ValueError('element {} has no parent ({} is regarded as none) '.format(p, q))
            p = q
        assert self._par[p] == p

        return p

    def _to_index_notation(self, i, j):
        v = self.N * j + i
        return v

    def _to_ij_notation(self, v):
        i = v % self.N
        j = int(v / self.N)
        return i, j

    def find_adj(self, element):  # find roots of distinct  components adjacent a element.
        ele_i, ele_j = self._to_ij_notation(element)
        adj_i = 0
        adj_j = 0
        adj_index = 0
        proper_adj_component_list = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                adj_i = ele_i + i
                adj_j = ele_j + j
                adj_index = self._to_index_notation(adj_i, adj_j)
                # check adj_index is proper adjacent to element
                if adj_index in self and adj_index != element:
                    # then adj_index is proper adjacent to element

                    root_of_the_adj = self._find_root(adj_index)
                    if root_of_the_adj not in proper_adj_component_list:
                        proper_adj_component_list.append(root_of_the_adj)
        return proper_adj_component_list

    def bfalg_add(self):
        """
        add new root index as root of one of tree in JSUFD
        and restore the if it is bifurcation points or not.
        :param :
        :return: none
        """

        # add a single disjoint element.

        if self._next >= self.N * self.M:
            return False

        single_disjoint_element = self.sorted_index_list[self._next]
        self._par[single_disjoint_element] = single_disjoint_element
        self._par_compressed_JSUFD[single_disjoint_element] = single_disjoint_element

        self._next += 1
        self.n_elts += 1
        self.n_comps += 1

        proper_adjacent_roots = self.find_adj(single_disjoint_element)
        self.leaf_elements[single_disjoint_element] = (len(proper_adjacent_roots) == 0)
        ret_bool = (len(proper_adjacent_roots) > 1)  # bifurcation point?
        self.bifurcation_elements[single_disjoint_element] = ret_bool
        # merge the components  into one
        for root in proper_adjacent_roots:
            assert root != single_disjoint_element
            self._par[root] = single_disjoint_element
            self._par_compressed_JSUFD[root] = single_disjoint_element
            self._is_root[root] = False

            self.n_comps -= 1
        self._is_root[single_disjoint_element] = True
