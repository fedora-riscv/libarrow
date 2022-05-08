# -*- sh-shell: rpm -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

%bcond_without use_flight
%bcond_with use_plasma
%bcond_with use_gandiva
%bcond_with use_mimalloc
%bcond_without use_ninja
# TODO: Enable this. This works on local but is fragile on GitHub Actions and
# Travis CI.
%bcond_with use_s3
%bcond_without have_rapidjson
%bcond_without have_re2
%bcond_without have_utf8proc

Name:		libarrow
Version:	8.0.0
Release:	1%{?dist}
Summary:	A toolbox for accelerated data interchange and in-memory processing
License:	ASL 2.0
URL:		https://arrow.apache.org/
Requires:	%{name}-doc = %{version}-%{release}
Source0:	https://dist.apache.org/repos/dist/release/arrow/arrow-%{version}/apache-arrow-%{version}.tar.gz
Patch0001:	0001-cpp-CMakeLists.txt.patch
Patch0002:	0002-cpp_src_arrow_util_utf8.h.patch
# Apache ORC (liborc) has numerous compile errors and apparently assumes
# a 64-bit build and runtime environment. This is only consumer of the liborc
# package, and in turn the only consumer of this and liborc is Ceph, which
# is also 64-bit only
ExcludeArch:	%{ix86} %{arm}
BuildRequires:	bison
BuildRequires:	boost-devel
BuildRequires:	brotli-devel
BuildRequires:	bzip2-devel
BuildRequires:	cmake
%if %{with use_ninja}
BuildRequires:	ninja-build
%endif
BuildRequires:	meson
%if %{with use_s3}
BuildRequires:	curl-devel
%endif
BuildRequires:	flex
BuildRequires:	gcc-c++
BuildRequires:	gflags-devel
BuildRequires:	glog-devel
BuildRequires:	grpc-devel
BuildRequires:	grpc-plugins
BuildRequires:	libzstd-devel
BuildRequires:	lz4-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	python3-devel
BuildRequires:	python3-numpy
BuildRequires:	xsimd-devel
BuildRequires:	abseil-cpp-devel
BuildRequires:	c-ares-devel
BuildRequires:	thrift-devel
%if %{with have_rapidjson}
BuildRequires:	rapidjson-devel
%endif
%if %{with have_re2}
BuildRequires:	re2-devel
%endif
BuildRequires:	snappy-devel
%if %{with have_utf8proc}
BuildRequires:	utf8proc-devel
%endif
BuildRequires:	zlib-devel
BuildRequires:	liborc-devel
%if %{with use_gandiva}
BuildRequires:	llvm-devel
BuildRequires:	ncurses-devel
%endif
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc

%description
Apache Arrow defines a language-independent columnar memory
format for flat and hierarchical data, organized for efficient
analytic operations on modern hardware like CPUs and GPUs. The
Arrow memory format also supports zero-copy reads for lightning-
fast data access without serialization overhead

%files
%{_libdir}/libarrow.so.*

#--------------------------------------------------------------------

%package doc
Summary:	Documentation files for Apache Arrow C++
BuildArch:	noarch

%description doc
Documentation files for Apache Arrow C++.

%files doc
%license LICENSE.txt
%doc README.md NOTICE.txt
%exclude %{_docdir}/arrow/

#--------------------------------------------------------------------

%package devel
Summary:	Libraries and header files for Apache Arrow C++
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	brotli-devel
Requires:	bzip2-devel
Requires:	libzstd-devel
Requires:	lz4-devel
Requires:	openssl-devel
%if %{with have_rapidjson}
Requires:	rapidjson-devel
%endif
%if %{with have_re2}
Requires:	re2-devel
%endif
Requires:	snappy-devel
%if %{with have_utf8proc}
Requires:	utf8proc-devel
%endif
Requires:	zlib-devel

%description devel
Libraries and header files for Apache Arrow C++.

%files devel
%dir %{_includedir}/arrow/
     %{_includedir}/arrow/*
%exclude %{_includedir}/arrow/dataset/
%if %{with use_flight}
%exclude %{_includedir}/arrow/flight/
%exclude %{_includedir}/arrow-flight-glib
%endif
%exclude %{_includedir}/arrow/python/
%exclude %{_libdir}/cmake/arrow/FindBrotli.cmake
%exclude %{_libdir}/cmake/arrow/FindLz4.cmake
%exclude %{_libdir}/cmake/arrow/FindORC.cmake
%exclude %{_libdir}/cmake/arrow/FindSnappy.cmake
%exclude %{_libdir}/cmake/arrow/FindgRPCAlt.cmake
%exclude %{_libdir}/cmake/arrow/Findre2Alt.cmake
%exclude %{_libdir}/cmake/arrow/Findutf8proc.cmake
%exclude %{_libdir}/cmake/arrow/Findzstd.cmake
%dir %{_libdir}/cmake/arrow/
     %{_libdir}/cmake/arrow/ArrowConfig*.cmake
     %{_libdir}/cmake/arrow/ArrowOptions.cmake
     %{_libdir}/cmake/arrow/ArrowTargets*.cmake
     %{_libdir}/cmake/arrow/FindArrow.cmake
     %{_libdir}/cmake/arrow/arrow-config.cmake
%{_libdir}/libarrow.so
%{_libdir}/pkgconfig/arrow-compute.pc
%{_libdir}/pkgconfig/arrow-csv.pc
%{_libdir}/pkgconfig/arrow-filesystem.pc
%{_libdir}/pkgconfig/arrow-json.pc
%{_libdir}/pkgconfig/arrow-orc.pc
%{_libdir}/pkgconfig/arrow.pc

#--------------------------------------------------------------------

%package dataset-libs
Summary:	C++ library to read and write semantic datasets
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description dataset-libs
This package contains the libraries for Apache Arrow dataset.

%files dataset-libs
%{_libdir}/libarrow_dataset.so.*

#--------------------------------------------------------------------

%package dataset-devel
Summary:	Libraries and header files for Apache Arrow dataset
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-dataset-libs%{?_isa} = %{version}-%{release}

%description dataset-devel
Libraries and header files for Apache Arrow dataset.

%files dataset-devel
%dir %{_includedir}/arrow/dataset/
     %{_includedir}/arrow/dataset/*
%{_libdir}/cmake/arrow/ArrowDatasetConfig*.cmake
%{_libdir}/cmake/arrow/ArrowDatasetTargets*.cmake
%{_libdir}/cmake/arrow/FindArrowDataset.cmake
%{_libdir}/libarrow_dataset.so
%{_libdir}/pkgconfig/arrow-dataset.pc

#--------------------------------------------------------------------

%if %{with use_flight}
%package flight-libs
Summary:	C++ library for fast data transport
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}
Requires:	openssl

%description flight-libs
This package contains the libraries for Apache Arrow Flight.

%files flight-libs
%{_libdir}/libarrow_flight.so.*
%{_libdir}/libarrow-flight-glib.so.*
%dir %{_libdir}/girepository-1.0/
     %{_libdir}/girepository-1.0/ArrowFlight-1.0.typelib

#--------------------------------------------------------------------

%package flight-devel
Summary:	Libraries and header files for Apache Arrow Flight
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-flight-libs%{?_isa} = %{version}-%{release}

%description flight-devel
Libraries and header files for Apache Arrow Flight.

%files flight-devel
%dir %{_includedir}/arrow/flight/
     %{_includedir}/arrow/flight/*
%dir %{_includedir}/arrow-flight-glib/
     %{_includedir}/arrow-flight-glib/*
%{_libdir}/cmake/arrow/ArrowFlightConfig*.cmake
%{_libdir}/cmake/arrow/ArrowFlightTargets*.cmake
%{_libdir}/cmake/arrow/FindArrowFlight.cmake
%{_libdir}/libarrow_flight.so
%{_libdir}/libarrow-flight-glib.so
%{_libdir}/pkgconfig/arrow-flight.pc
%{_libdir}/pkgconfig/arrow-flight-glib.pc
%endif

#--------------------------------------------------------------------

%if %{with use_gandiva}
%package -n gandiva-libs
Summary:	C++ library for compiling and evaluating expressions
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}
Requires:	ncurses-libs

%description -n gandiva-libs
This package contains the libraries for Gandiva.

%files -n gandiva-libs
%{_libdir}/libgandiva.so.*

#--------------------------------------------------------------------

%package -n gandiva-devel
Summary:	Libraries and header files for Gandiva
Requires:	gandiva-libs%{?_isa} = %{version}-%{release}
Requires:	llvm-devel

%description -n gandiva-devel
Libraries and header files for Gandiva.

%files -n gandiva-devel
%dir %{_includedir}/gandiva/
     %{_includedir}/gandiva/
%{_libdir}/cmake/arrow/GandivaConfig*.cmake
%{_libdir}/cmake/arrow/GandivaTargets*.cmake
%{_libdir}/cmake/arrow/FindGandiva.cmake
%{_libdir}/libgandiva.so
%{_libdir}/pkgconfig/gandiva.pc
%endif

#--------------------------------------------------------------------

%package python-libs
Summary:	Python integration library for Apache Arrow
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	python3-numpy

%description python-libs
This package contains the Python integration library for Apache Arrow.

%files python-libs
%{_libdir}/libarrow_python.so.*

#--------------------------------------------------------------------

%package python-devel
Summary:	Libraries and header files for Python integration library
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Requires:	%{name}-python-libs%{?_isa} = %{version}-%{release}
Requires:	python3-devel

%description python-devel
Libraries and header files for Python integration library for Apache Arrow.

%files python-devel
%dir %{_includedir}/arrow/python/
     %{_includedir}/arrow/python/*
%exclude %{_includedir}/arrow/python/flight.h
%{_libdir}/cmake/arrow/ArrowPythonConfig*.cmake
%{_libdir}/cmake/arrow/ArrowPythonTargets*.cmake
%{_libdir}/cmake/arrow/FindArrowPython.cmake
%{_libdir}/libarrow_python.so
%{_libdir}/pkgconfig/arrow-python.pc

#--------------------------------------------------------------------

%if %{with use_flight}
%package python-flight-libs
Summary:	Python integration library for Apache Arrow Flight
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-flight-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-python-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description python-flight-libs
This package contains the Python integration library for Apache Arrow Flight.

%files python-flight-libs
%{_libdir}/libarrow_python_flight.so.*

#--------------------------------------------------------------------

%package python-flight-devel
Summary:	Libraries and header files for Python integration
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-flight-devel%{?_isa} = %{version}-%{release}
Requires:	%{name}-python-devel%{?_isa} = %{version}-%{release}
Requires:	%{name}-python-flight-libs%{?_isa} = %{version}-%{release}

%description python-flight-devel
Libraries and header files for Python integration library for
Apache Arrow Flight.

%files python-flight-devel
%{_includedir}/arrow/python/flight.h
%{_libdir}/cmake/arrow/ArrowPythonFlightConfig*.cmake
%{_libdir}/cmake/arrow/ArrowPythonFlightTargets*.cmake
%{_libdir}/cmake/arrow/FindArrowPythonFlight.cmake
%{_libdir}/libarrow_python_flight.so
%{_libdir}/pkgconfig/arrow-python-flight.pc
%endif

%if %{with use_plasma}
#--------------------------------------------------------------------

%package -n plasma-libs
Summary:	Runtime libraries for Plasma in-memory object store
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description -n plasma-libs
This package contains the libraries for Plasma in-memory object store.

%files -n plasma-libs
%{_libdir}/libplasma.so.*

#--------------------------------------------------------------------

%package -n plasma-store-server
Summary:	Server for Plasma in-memory object store
Requires:	plasma-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description -n plasma-store-server
This package contains the server for Plasma in-memory object store.

%files -n plasma-store-server
%{_bindir}/plasma-store-server

#--------------------------------------------------------------------

%package -n plasma-libs-devel
Summary:	Libraries and header files for Plasma in-memory object store
Requires:	plasma-libs%{?_isa} = %{version}-%{release}
# plasma-devel a.k.a. kdelibs-devel provides
# conflicts with all versions of plasma-devel %%{_libdir}/libplasma.so
BuildConflicts: plasma-devel 
# conflicts with all versions of plasma-workspace-devel %%{_includedir}/*
BuildConflicts: plasma-workspace-devel

%description -n plasma-libs-devel
Libraries and header files for Plasma in-memory object store.

%files -n plasma-libs-devel
%dir %{_includedir}/plasma/
     %{_includedir}/plasma/*
%{_libdir}/cmake/arrow/PlasmaConfig*.cmake
%{_libdir}/cmake/arrow/PlasmaTargets*.cmake
%{_libdir}/cmake/arrow/FindPlasma.cmake
%{_libdir}/libplasma.so
%{_libdir}/pkgconfig/plasma*.pc

%endif
#--------------------------------------------------------------------

%package -n parquet-libs
Summary:	Runtime libraries for Apache Parquet C++
Requires:	boost-program-options
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}
Requires:	openssl

%description -n parquet-libs
This package contains the libraries for Apache Parquet C++.

%files -n parquet-libs
%{_libdir}/libparquet.so.*

#--------------------------------------------------------------------

%package -n parquet-libs-devel
Summary:	Libraries and header files for Apache Parquet C++
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	parquet-libs%{?_isa} = %{version}-%{release}
Requires:	zlib-devel

%description -n parquet-libs-devel
Libraries and header files for Apache Parquet C++.

%files -n parquet-libs-devel
%dir %{_includedir}/parquet/
     %{_includedir}/parquet/*
%{_libdir}/cmake/arrow/ParquetConfig*.cmake
%{_libdir}/cmake/arrow/ParquetTargets*.cmake
%{_libdir}/cmake/arrow/FindParquet.cmake
%{_libdir}/libparquet.so
%{_libdir}/pkgconfig/parquet*.pc

#--------------------------------------------------------------------

%package glib-libs
Summary:	Runtime libraries for Apache Arrow GLib
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description glib-libs
This package contains the libraries for Apache Arrow GLib.

%files glib-libs
%{_libdir}/libarrow-glib.so.*
%dir %{_libdir}/girepository-1.0/
     %{_libdir}/girepository-1.0/Arrow-1.0.typelib
%exclude %{_datadir}/doc/arrow-glib/*

#--------------------------------------------------------------------

%package glib-devel
Summary:	Libraries and header files for Apache Arrow GLib
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Requires:	%{name}-glib-libs%{?_isa} = %{version}-%{release}
Requires:	glib2-devel
Requires:	gobject-introspection-devel

%description glib-devel
Libraries and header files for Apache Arrow GLib.

%files glib-devel
%dir %{_includedir}/arrow-glib/
     %{_includedir}/arrow-glib/*
%{_libdir}/libarrow-glib.so
%{_libdir}/pkgconfig/arrow-glib.pc
%{_libdir}/pkgconfig/arrow-orc-glib.pc
%dir %{_datadir}/arrow-glib/
     %{_datadir}/arrow-glib/example/*
%dir %{_datadir}/gir-1.0/
     %{_datadir}/gir-1.0/Arrow-1.0.gir
     %{_datadir}/gir-1.0/ArrowFlight-1.0.gir

#--------------------------------------------------------------------

%package glib-doc
Summary:	Documentation for Apache Arrow GLib

%description glib-doc
Documentation for Apache Arrow GLib.

%files glib-doc
%dir %{_datadir}/gtk-doc/
%dir %{_datadir}/gtk-doc/html/
%dir %{_datadir}/gtk-doc/html/arrow-glib/
     %{_datadir}/gtk-doc/html/arrow-glib/*
%dir %{_datadir}/gtk-doc/html/arrow-flight-glib/
     %{_datadir}/gtk-doc/html/arrow-flight-glib/*

#--------------------------------------------------------------------

%package dataset-glib-libs
Summary:	Runtime libraries for Apache Arrow dataset GLib
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-dataset-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-glib-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description dataset-glib-libs
This package contains the libraries for Apache Arrow dataset GLib.

%files dataset-glib-libs
%{_libdir}/libarrow-dataset-glib.so.*
%dir %{_libdir}/girepository-1.0/
     %{_libdir}/girepository-1.0/ArrowDataset-1.0.typelib

#--------------------------------------------------------------------

%package dataset-glib-devel
Summary:	Libraries and header files for Apache Arrow dataset GLib
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-dataset-devel%{?_isa} = %{version}-%{release}
Requires:	%{name}-glib-devel%{?_isa} = %{version}-%{release}
Requires:	%{name}-dataset-glib-libs%{?_isa} = %{version}-%{release}

%description dataset-glib-devel
Libraries and header files for Apache Arrow dataset GLib.

%files dataset-glib-devel
%dir %{_includedir}/arrow-dataset-glib/
     %{_includedir}/arrow-dataset-glib/*
%{_libdir}/libarrow-dataset-glib.so
%{_libdir}/pkgconfig/arrow-dataset-glib.pc
%dir %{_datadir}/gir-1.0/
     %{_datadir}/gir-1.0/ArrowDataset-1.0.gir

#--------------------------------------------------------------------

%package dataset-glib-doc
Summary:	Documentation for Apache Arrow dataset GLib

%description dataset-glib-doc
Documentation for Apache Arrow dataset GLib.

%files dataset-glib-doc
%dir %{_datadir}/gtk-doc/html/arrow-dataset-glib/
     %{_datadir}/gtk-doc/html/arrow-dataset-glib/*

#--------------------------------------------------------------------

%if %{with use_gandiva}
%package -n gandiva-glib-libs
Summary:	Runtime libraries for Gandiva GLib
Requires:	gandiva-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-glib-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description -n gandiva-glib-libs
This package contains the libraries for Gandiva GLib.

%files -n gandiva-glib-libs
%{_libdir}/libgandiva-glib.so.*
%dir %{_libdir}/girepository-1.0/
     %{_libdir}/girepository-1.0/Gandiva-1.0.typelib

#--------------------------------------------------------------------

%package -n gandiva-glib-devel
Summary:	Libraries and header files for Gandiva GLib
Requires:	gandiva-devel%{?_isa} = %{version}-%{release}
Requires:	%{name}-glib-devel%{?_isa} = %{version}-%{release}

%description -n gandiva-glib-devel
Libraries and header files for Gandiva GLib.

%files -n gandiva-glib-devel
%dir %{_includedir}/gandiva-glib/
     %{_includedir}/gandiva-glib/*
%{_libdir}/libgandiva-glib.so
%{_libdir}/pkgconfig/gandiva-glib.pc
%dir %{_datadir}/gir-1.0/
     %{_datadir}/gir-1.0/Gandiva-1.0.gir

#--------------------------------------------------------------------

%package -n gandiva-glib-doc
Summary:	Documentation for Gandiva GLib

%description -n gandiva-glib-doc
Documentation for Gandiva GLib.

%files -n gandiva-glib-doc
%dir %{_datadir}/gtk-doc/html/gandiva-glib/
     %{_datadir}/gtk-doc/html/gandiva-glib/*
%endif

%if %{with use_plasma}
#--------------------------------------------------------------------

%package -n plasma-glib-libs
Summary:	Runtime libraries for Plasma GLib
Requires:	plasma-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-glib-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description -n plasma-glib-libs
This package contains the libraries for Plasma GLib.

%files -n plasma-glib-libs
%{_libdir}/libplasma-glib.so.*
%dir %{_libdir}/girepository-1.0/
     %{_libdir}/girepository-1.0/Plasma-1.0.typelib

#--------------------------------------------------------------------

%package -n plasma-glib-devel
Summary:	Libraries and header files for Plasma GLib
Requires:	plasma-devel%{?_isa} = %{version}-%{release}
Requires:	plasma-glib-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-glib-devel%{?_isa} = %{version}-%{release}

%description -n plasma-glib-devel
Libraries and header files for Plasma GLib.

%files -n plasma-glib-devel
%dir %{_includedir}/plasma-glib/
     %{_includedir}/plasma-glib/*
%{_libdir}/libplasma-glib.so
%{_libdir}/pkgconfig/plasma-glib.pc
%dir %{_datadir}/gir-1.0/
     %{_datadir}/gir-1.0/Plasma-1.0.gir

#--------------------------------------------------------------------

%package -n plasma-glib-doc
Summary:	Documentation for Plasma GLib

%description -n plasma-glib-doc
Documentation for Plasma GLib.

%files -n plasma-glib-doc
%dir %{_datadir}/gtk-doc/html/plasma-glib/
     %{_datadir}/gtk-doc/html/plasma-glib/*
%endif

#--------------------------------------------------------------------

%package -n parquet-glib-libs
Summary:	Runtime libraries for Apache Parquet GLib
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	parquet-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-glib-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description -n parquet-glib-libs
This package contains the libraries for Apache Parquet GLib.

%files -n parquet-glib-libs
%{_libdir}/libparquet-glib.so.*
%dir %{_libdir}/girepository-1.0/
     %{_libdir}/girepository-1.0/Parquet-1.0.typelib

#--------------------------------------------------------------------

%package -n parquet-glib-devel
Summary:	Libraries and header files for Apache Parquet GLib
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	parquet-libs-devel%{?_isa} = %{version}-%{release}
Requires:	parquet-glib-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-glib-devel%{?_isa} = %{version}-%{release}

%description -n parquet-glib-devel
Libraries and header files for Apache Parquet GLib.

%files -n parquet-glib-devel
%dir %{_includedir}/parquet-glib/
     %{_includedir}/parquet-glib/*
%{_libdir}/libparquet-glib.so
%{_libdir}/pkgconfig/parquet-glib.pc
%dir %{_datadir}/gir-1.0/
     %{_datadir}/gir-1.0/Parquet-1.0.gir

#--------------------------------------------------------------------

%package -n parquet-glib-doc
Summary:	Documentation for Apache Parquet GLib

%description -n parquet-glib-doc
Documentation for Apache Parquet GLib.

%files -n parquet-glib-doc
%dir %{_datadir}/gtk-doc/html/parquet-glib/
     %{_datadir}/gtk-doc/html/parquet-glib/*

#--------------------------------------------------------------------

%prep
%autosetup -p1 -n apache-arrow-%{version}

%build
pushd cpp
%cmake \
%if %{with use_flight}
  -DARROW_FLIGHT:BOOL=ON \
%endif
%if %{with use_gandiva}
  -DARROW_GANDIVA:BOOL=ON \
%endif
%if %{with use_mimalloc}
  -DARROW_MIMALLOC:BOOL=ON \
%endif
  -DARROW_ORC=ON \
  -DARROW_PARQUET:BOOL=ON \
%if %{with use_plasma}
  -DARROW_PLASMA:BOOL=ON \
%endif
  -DARROW_PYTHON:BOOL=ON \
  -DARROW_JEMALLOC:BOOL=OFF \
  -DGRPC_SOURCE="SYSTEM" \
  -Dxsimd_SOURCE="SYSTEM" \
%if %{with use_s3}
  -DARROW_S3:BOOL=ON \
%endif
  -DARROW_WITH_BROTLI:BOOL=ON \
  -DARROW_WITH_BZ2:BOOL=ON \
  -DARROW_WITH_LZ4:BOOL=ON \
  -DARROW_WITH_SNAPPY:BOOL=ON \
  -DARROW_WITH_ZLIB:BOOL=ON \
  -DARROW_WITH_ZSTD:BOOL=ON \
  -DARROW_WITH_XSIMD:BOOL=ON \
  -DARROW_BUILD_STATIC:BOOL=OFF \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_COLOR_MAKEFILE:BOOL=OFF \
  -DARROW_USE_CCACHE:BOOL=OFF \
  -DCMAKE_UNITY_BUILD:BOOL=ON \
  -DPARQUET_REQUIRE_ENCRYPTION:BOOL=ON \
  -DPythonInterp_FIND_VERSION:BOOL=ON \
  -DPythonInterp_FIND_VERSION_MAJOR=3 \
%if %{with use_ninja}
  -GNinja
%endif

export VERBOSE=1
export GCC_COLORS=
%cmake_build
popd

pushd c_glib
%meson \
  -Darrow_cpp_build_dir=../cpp/%{_vpath_builddir} \
  -Darrow_cpp_build_type=relwithdebinfo \
  -Dgtk_doc=true
%meson_build

#--------------------------------------------------------------------

%install
pushd c_glib
%meson_install
popd

pushd cpp
%cmake_install
popd

#--------------------------------------------------------------------

%changelog
* Sun May 8 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 8.0.0-1
- Arrow 8.0.0 GA

* Thu Jan 13 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 7.0.0-1
- New upstream release.

