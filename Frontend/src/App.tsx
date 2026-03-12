import { useState } from 'react';
import AdminDashboard from './components/admin/AdminDashboard';
import { Menu, X, Phone, Mail, MapPin, GraduationCap, Users, Award, BookOpen, Microscope, Building2, ChevronRight } from 'lucide-react';
import { Chatbot } from './components/Chatbot';
import { ImageWithFallback } from './components/figma/ImageWithFallback';

export default function App() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    element?.scrollIntoView({ behavior: 'smooth' });
    setMobileMenuOpen(false);
  };

  const programs = [
    {
      name: 'Computer Science & Engineering',
      duration: '4 Years',
      description: 'Master programming, AI, machine learning, and software development with industry-standard practices.',
      icon: '💻'
    },
    {
      name: 'Electronics & Communication Engineering',
      duration: '4 Years',
      description: 'Learn about circuits, communication systems, embedded systems, and signal processing.',
      icon: '📡'
    },
    {
      name: 'Mechanical Engineering',
      duration: '4 Years',
      description: 'Study thermodynamics, manufacturing, robotics, and mechanical design principles.',
      icon: '⚙️'
    },
    {
      name: 'Civil Engineering',
      duration: '4 Years',
      description: 'Focus on construction, structural design, urban planning, and infrastructure development.',
      icon: '🏗️'
    },
    {
      name: 'Electrical & Electronics Engineering',
      duration: '4 Years',
      description: 'Explore power systems, control systems, renewable energy, and electrical machines.',
      icon: '⚡'
    }
  ];

  const facilities = [
    {
      title: 'Modern Laboratories',
      description: 'State-of-the-art labs equipped with latest technology and equipment for hands-on learning.',
      icon: <Microscope className="w-8 h-8" />
    },
    {
      title: 'Central Library',
      description: '50,000+ books, digital resources, journals, and 24/7 e-library access for students.',
      icon: <BookOpen className="w-8 h-8" />
    },
    {
      title: 'Smart Classrooms',
      description: 'Technology-enabled classrooms with projectors, smart boards, and interactive learning tools.',
      icon: <GraduationCap className="w-8 h-8" />
    },
    {
      title: 'Sports Complex',
      description: 'Comprehensive sports facilities including cricket, football, basketball, gym, and indoor games.',
      icon: <Award className="w-8 h-8" />
    },
    {
      title: 'Hostel Facilities',
      description: 'Separate hostels for boys and girls with 24/7 security, WiFi, and mess facilities.',
      icon: <Building2 className="w-8 h-8" />
    },
    {
      title: 'Placement Cell',
      description: '85%+ placement rate with top companies. Dedicated training and career guidance.',
      icon: <Users className="w-8 h-8" />
    }
  ];

  const stats = [
    { number: '5000+', label: 'Students' },
    { number: '200+', label: 'Faculty Members' },
    { number: '85%', label: 'Placement Rate' },
    { number: '50+', label: 'Years of Excellence' }
  ];

  // Route to admin dashboard
  if (window.location.pathname === '/admin') {
    return <AdminDashboard />;
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="bg-white shadow-md sticky top-0 z-40">
        <nav className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="bg-blue-600 rounded-lg p-2">
                <GraduationCap className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">St Lourdes</h1>
                <p className="text-xs text-gray-600">Engineering College</p>
              </div>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-8">
              <button onClick={() => scrollToSection('home')} className="text-gray-700 hover:text-blue-600 transition-colors">
                Home
              </button>
              <button onClick={() => scrollToSection('about')} className="text-gray-700 hover:text-blue-600 transition-colors">
                About
              </button>
              <button onClick={() => scrollToSection('programs')} className="text-gray-700 hover:text-blue-600 transition-colors">
                Programs
              </button>
              <button onClick={() => scrollToSection('admissions')} className="text-gray-700 hover:text-blue-600 transition-colors">
                Admissions
              </button>
              <button onClick={() => scrollToSection('facilities')} className="text-gray-700 hover:text-blue-600 transition-colors">
                Facilities
              </button>
              <button onClick={() => scrollToSection('contact')} className="text-gray-700 hover:text-blue-600 transition-colors">
                Contact
              </button>
              <button 
                onClick={() => scrollToSection('admissions')}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Apply Now
              </button>
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 rounded-lg hover:bg-gray-100"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

          {/* Mobile Navigation */}
          {mobileMenuOpen && (
            <div className="md:hidden py-4 space-y-2">
              <button onClick={() => scrollToSection('home')} className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                Home
              </button>
              <button onClick={() => scrollToSection('about')} className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                About
              </button>
              <button onClick={() => scrollToSection('programs')} className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                Programs
              </button>
              <button onClick={() => scrollToSection('admissions')} className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                Admissions
              </button>
              <button onClick={() => scrollToSection('facilities')} className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                Facilities
              </button>
              <button onClick={() => scrollToSection('contact')} className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                Contact
              </button>
              <button 
                onClick={() => scrollToSection('admissions')}
                className="block w-full text-left px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Apply Now
              </button>
            </div>
          )}
        </nav>
      </header>

      {/* Hero Section */}
      <section id="home" className="relative h-[600px] bg-gray-900">
        <img
          src="https://images.unsplash.com/photo-1695204651916-a300caba0d7e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxlbmdpbmVlcmluZyUyMGNvbGxlZ2UlMjBjYW1wdXN8ZW58MXx8fHwxNzY5NDEzMzQ0fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
          alt="St Lourdes Engineering College Campus"
          className="absolute inset-0 w-full h-full object-cover opacity-60"
        />
        <div className="relative container mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center">
          <div className="max-w-3xl text-white">
            <h1 className="text-5xl md:text-6xl mb-6">Welcome to St Lourdes Engineering College</h1>
            <p className="text-xl md:text-2xl mb-8 text-gray-200">
              Shaping Future Engineers with Excellence in Education and Innovation
            </p>
            <div className="flex flex-wrap gap-4">
              <button 
                onClick={() => scrollToSection('admissions')}
                className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors text-lg"
              >
                Apply for Admission 2026
              </button>
              <button 
                onClick={() => scrollToSection('programs')}
                className="bg-white text-gray-900 px-8 py-3 rounded-lg hover:bg-gray-100 transition-colors text-lg"
              >
                Explore Programs
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-blue-600 text-white py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-4xl md:text-5xl mb-2">{stat.number}</div>
                <div className="text-blue-100">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-20 bg-gray-50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl mb-6 text-gray-900">About St Lourdes</h2>
              <p className="text-gray-700 mb-4 text-lg">
                Established in 1976, St Lourdes Engineering College has been a beacon of excellence in technical education for over five decades. We are committed to providing world-class engineering education that combines theoretical knowledge with practical skills.
              </p>
              <p className="text-gray-700 mb-4 text-lg">
                Our state-of-the-art infrastructure, experienced faculty, and industry partnerships ensure that our students are well-prepared for the challenges of the modern engineering world.
              </p>
              <p className="text-gray-700 mb-6 text-lg">
                Accredited by NAAC with 'A' grade and approved by AICTE, we offer undergraduate and postgraduate programs in various engineering disciplines.
              </p>
              <div className="flex flex-wrap gap-4">
                <div className="flex items-center gap-2 bg-white px-4 py-2 rounded-lg shadow-sm">
                  <Award className="w-5 h-5 text-blue-600" />
                  <span className="text-gray-700">NAAC 'A' Accredited</span>
                </div>
                <div className="flex items-center gap-2 bg-white px-4 py-2 rounded-lg shadow-sm">
                  <Award className="w-5 h-5 text-blue-600" />
                  <span className="text-gray-700">AICTE Approved</span>
                </div>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <ImageWithFallback
                src="https://images.unsplash.com/photo-1733426509854-10931d84009a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxlbmdpbmVlcmluZyUyMGxhYm9yYXRvcnklMjBzdHVkZW50c3xlbnwxfHx8fDE3Njk0MTMzNDR8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
                alt="Students in laboratory"
                className="rounded-lg shadow-lg h-64 object-cover"
              />
              <ImageWithFallback
                src="https://images.unsplash.com/photo-1721552023489-6c2ec21d297f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx1bml2ZXJzaXR5JTIwbGlicmFyeSUyMGJvb2tzfGVufDF8fHx8MTc2OTQxMzM0NXww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
                alt="Library"
                className="rounded-lg shadow-lg h-64 object-cover mt-8"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Programs Section */}
      <section id="programs" className="py-20 bg-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl mb-4 text-gray-900">Our Programs</h2>
            <p className="text-gray-600 text-lg max-w-2xl mx-auto">
              Choose from our wide range of B.Tech programs designed to shape the future of engineering
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {programs.map((program, index) => (
              <div key={index} className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-xl transition-shadow">
                <div className="text-4xl mb-4">{program.icon}</div>
                <h3 className="text-xl mb-2 text-gray-900">{program.name}</h3>
                <div className="flex items-center gap-2 text-blue-600 mb-3">
                  <BookOpen className="w-4 h-4" />
                  <span className="text-sm">{program.duration}</span>
                </div>
                <p className="text-gray-600 mb-4">{program.description}</p>
                <button className="text-blue-600 hover:text-blue-700 flex items-center gap-1 group">
                  Learn More
                  <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Admissions Section */}
      <section id="admissions" className="py-20 bg-blue-50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-4xl mb-4 text-gray-900">Admissions 2026-27</h2>
              <p className="text-gray-600 text-lg">
                Join St Lourdes Engineering College and become part of our legacy of excellence
              </p>
            </div>
            
            <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
              <h3 className="text-2xl mb-6 text-gray-900">Admission Process</h3>
              <div className="space-y-6">
                <div className="flex gap-4">
                  <div className="bg-blue-600 text-white rounded-full w-10 h-10 flex items-center justify-center flex-shrink-0">
                    1
                  </div>
                  <div>
                    <h4 className="text-lg mb-1 text-gray-900">Online Application</h4>
                    <p className="text-gray-600">Fill out the online application form on our admissions portal with your academic details.</p>
                  </div>
                </div>
                <div className="flex gap-4">
                  <div className="bg-blue-600 text-white rounded-full w-10 h-10 flex items-center justify-center flex-shrink-0">
                    2
                  </div>
                  <div>
                    <h4 className="text-lg mb-1 text-gray-900">Document Submission</h4>
                    <p className="text-gray-600">Upload required documents including mark sheets, entrance exam scores, and ID proof.</p>
                  </div>
                </div>
                <div className="flex gap-4">
                  <div className="bg-blue-600 text-white rounded-full w-10 h-10 flex items-center justify-center flex-shrink-0">
                    3
                  </div>
                  <div>
                    <h4 className="text-lg mb-1 text-gray-900">Review & Selection</h4>
                    <p className="text-gray-600">Applications are reviewed based on academic merit and entrance exam scores.</p>
                  </div>
                </div>
                <div className="flex gap-4">
                  <div className="bg-blue-600 text-white rounded-full w-10 h-10 flex items-center justify-center flex-shrink-0">
                    4
                  </div>
                  <div>
                    <h4 className="text-lg mb-1 text-gray-900">Enrollment</h4>
                    <p className="text-gray-600">Selected candidates will receive admission offer and can complete enrollment formalities.</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6 mb-8">
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h4 className="text-xl mb-4 text-gray-900">Eligibility Criteria</h4>
                <ul className="space-y-2 text-gray-600">
                  <li className="flex items-start gap-2">
                    <ChevronRight className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                    <span>Completed 10+2 with PCM</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <ChevronRight className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                    <span>Minimum 60% aggregate marks</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <ChevronRight className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                    <span>Valid JEE Main or State CET score</span>
                  </li>
                </ul>
              </div>
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h4 className="text-xl mb-4 text-gray-900">Important Dates</h4>
                <ul className="space-y-2 text-gray-600">
                  <li className="flex justify-between">
                    <span>Application Opens:</span>
                    <span className="text-gray-900">March 1, 2026</span>
                  </li>
                  <li className="flex justify-between">
                    <span>Application Deadline:</span>
                    <span className="text-gray-900">June 30, 2026</span>
                  </li>
                  <li className="flex justify-between">
                    <span>Classes Begin:</span>
                    <span className="text-gray-900">August 15, 2026</span>
                  </li>
                </ul>
              </div>
            </div>

            <div className="text-center">
              <button className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors text-lg">
                Start Your Application
              </button>
              <p className="mt-4 text-gray-600">
                Have questions? Use our chatbot assistant or call us at +1-555-0123
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Facilities Section */}
      <section id="facilities" className="py-20 bg-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl mb-4 text-gray-900">World-Class Facilities</h2>
            <p className="text-gray-600 text-lg max-w-2xl mx-auto">
              Our campus is equipped with modern infrastructure to support your academic and personal growth
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {facilities.map((facility, index) => (
              <div key={index} className="bg-gray-50 rounded-lg p-6 hover:shadow-lg transition-shadow">
                <div className="text-blue-600 mb-4">{facility.icon}</div>
                <h3 className="text-xl mb-2 text-gray-900">{facility.title}</h3>
                <p className="text-gray-600">{facility.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Campus Life Section */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl mb-4 text-gray-900">Campus Life</h2>
            <p className="text-gray-600 text-lg max-w-2xl mx-auto">
              Experience a vibrant campus culture with numerous opportunities for growth and development
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <ImageWithFallback
                src="https://images.unsplash.com/photo-1723987135977-ae935608939e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb21wdXRlciUyMHNjaWVuY2UlMjBjbGFzc3Jvb218ZW58MXx8fHwxNzY5MzI5NTc2fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
                alt="Classroom"
                className="w-full h-64 object-cover rounded-lg shadow-lg mb-4"
              />
              <h3 className="text-xl mb-2 text-gray-900">Academic Excellence</h3>
              <p className="text-gray-600">Interactive learning environment with experienced faculty and modern teaching methods</p>
            </div>
            <div className="text-center">
              <ImageWithFallback
                src="https://images.unsplash.com/photo-1733426509854-10931d84009a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxlbmdpbmVlcmluZyUyMGxhYm9yYXRvcnklMjBzdHVkZW50c3xlbnwxfHx8fDE3Njk0MTMzNDR8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
                alt="Laboratory"
                className="w-full h-64 object-cover rounded-lg shadow-lg mb-4"
              />
              <h3 className="text-xl mb-2 text-gray-900">Hands-On Learning</h3>
              <p className="text-gray-600">State-of-the-art laboratories for practical experience and research opportunities</p>
            </div>
            <div className="text-center">
              <ImageWithFallback
                src="https://images.unsplash.com/photo-1721552023489-6c2ec21d297f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx1bml2ZXJzaXR5JTIwbGlicmFyeSUyMGJvb2tzfGVufDF8fHx8MTc2OTQxMzM0NXww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
                alt="Library"
                className="w-full h-64 object-cover rounded-lg shadow-lg mb-4"
              />
              <h3 className="text-xl mb-2 text-gray-900">Rich Resources</h3>
              <p className="text-gray-600">Extensive library and digital resources to support your learning journey</p>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-20 bg-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl mb-4 text-gray-900">Get In Touch</h2>
            <p className="text-gray-600 text-lg">
              We're here to help you with any questions about admissions or academics
            </p>
          </div>
          <div className="max-w-4xl mx-auto grid md:grid-cols-3 gap-8">
            <div className="text-center p-6 bg-gray-50 rounded-lg">
              <Phone className="w-8 h-8 text-blue-600 mx-auto mb-4" />
              <h3 className="text-lg mb-2 text-gray-900">Phone</h3>
              <p className="text-gray-600">+1-555-0123</p>
              <p className="text-gray-600">+1-555-0124</p>
            </div>
            <div className="text-center p-6 bg-gray-50 rounded-lg">
              <Mail className="w-8 h-8 text-blue-600 mx-auto mb-4" />
              <h3 className="text-lg mb-2 text-gray-900">Email</h3>
              <p className="text-gray-600">admissions@stlourdes.edu</p>
              <p className="text-gray-600">info@stlourdes.edu</p>
            </div>
            <div className="text-center p-6 bg-gray-50 rounded-lg">
              <MapPin className="w-8 h-8 text-blue-600 mx-auto mb-4" />
              <h3 className="text-lg mb-2 text-gray-900">Address</h3>
              <p className="text-gray-600">Knowledge Park</p>
              <p className="text-gray-600">City 560001</p>
            </div>
          </div>
          <div className="mt-12 text-center">
            <p className="text-gray-600 mb-4">
              Office Hours: Monday - Saturday, 9:00 AM - 5:00 PM
            </p>
            <p className="text-blue-600">
              Try our AI chatbot for instant answers to your questions!
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="bg-blue-600 rounded-lg p-2">
                  <GraduationCap className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="font-bold">St Lourdes</h3>
                  <p className="text-xs text-gray-400">Engineering College</p>
                </div>
              </div>
              <p className="text-gray-400 text-sm">
                Shaping future engineers with excellence in education and innovation since 1976.
              </p>
            </div>
            <div>
              <h4 className="mb-4">Quick Links</h4>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li><button onClick={() => scrollToSection('about')} className="hover:text-white">About Us</button></li>
                <li><button onClick={() => scrollToSection('programs')} className="hover:text-white">Programs</button></li>
                <li><button onClick={() => scrollToSection('admissions')} className="hover:text-white">Admissions</button></li>
                <li><button onClick={() => scrollToSection('facilities')} className="hover:text-white">Facilities</button></li>
              </ul>
            </div>
            <div>
              <h4 className="mb-4">Programs</h4>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li className="hover:text-white">Computer Science</li>
                <li className="hover:text-white">Electronics & Communication</li>
                <li className="hover:text-white">Mechanical Engineering</li>
                <li className="hover:text-white">Civil Engineering</li>
              </ul>
            </div>
            <div>
              <h4 className="mb-4">Contact</h4>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li>+1-555-0123</li>
                <li>admissions@stlourdes.edu</li>
                <li>Knowledge Park, City 560001</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-8 text-center text-gray-400 text-sm">
            <p>&copy; 2026 St Lourdes Engineering College. All rights reserved.</p>
          </div>
        </div>
      </footer>

      {/* Chatbot */}
      <Chatbot />
    </div>
  );
}